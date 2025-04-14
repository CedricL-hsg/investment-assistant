import pandas as pd
from yahooquery import Ticker
from src.utils import fetch_live_macro_data, load_macro_classification, classify_market_regime
from src.portfolio_generator import load_asset_allocation, load_asset_list, generate_portfolios
from src.monte_carlo import run_monte_carlo
from src.visualization import plot_monte_carlo, plot_portfolio_allocation, plot_asset_averages
from src.simulation_analyzer import analyze_simulation_results

# ===========================
# 1. Makro-Daten und Regime
# ===========================
live_macro_data = fetch_live_macro_data()
macro_classification = load_macro_classification()

print("\n📊 Aktuelle Makrodaten von FRED:")
print(live_macro_data.to_string(index=False))
print("\n")

regime = classify_market_regime(live_macro_data, macro_classification)
print(f"Aktuelles Marktregime: {regime}")

# ===========================
# 2. Strategie Auswahl
# ===========================
print("Bitte wähle eine Anlagestrategie:")
print("1 - Konservativ")
print("2 - Ausgewogen")
print("3 - Wachstum")

strategie_input = input("Deine Wahl (1/2/3): ")
strategie_mapping = {'1': 'Konservativ', '2': 'Ausgewogen', '3': 'Wachstum'}
strategie = strategie_mapping.get(strategie_input, 'Ausgewogen')

print(f"✅ Du hast die Strategie '{strategie}' gewählt.\n")

# ===========================
# 3. Zeitraum-Auswahl (3 Zeiträume)
# ===========================
date_ranges = []

for i in range(1, 4):
    print(f"🔢 Zeitraum {i}:")
    start_date = input(f"Gib Startdatum {i} ein (Format: YYYY-MM-DD): ")
    end_date = input(f"Gib Enddatum {i} ein (Format: YYYY-MM-DD): ")
    date_ranges.append((start_date, end_date))

print(f"\n🧩 Gewählte Zeiträume: {date_ranges}\n")

# ===========================
# 4. Asset Allocation laden
# ===========================
asset_allocation_df = load_asset_allocation()
current_allocation = asset_allocation_df[
    (asset_allocation_df['Makro_Regime'] == regime) &
    (asset_allocation_df['Strategie'] == strategie)
].iloc[0].drop(['Makro_Regime', 'Strategie'])

print("✅ Deine gewählte Asset-Allokation:")
print(current_allocation)
print("\n")

# ===========================
# 5. Asset-Liste laden
# ===========================
asset_list = load_asset_list()
assets_by_class = asset_list.groupby('Class')['Asset'].apply(list).to_dict()

# ===========================
# 6. Portfolios generieren
# ===========================
portfolios = generate_portfolios(current_allocation, assets_by_class)
portfolios.to_csv('data/processed/generated_portfolios.csv', index=False)
print("✅ Portfolios erfolgreich generiert und gespeichert.")

# ===========================
# 7. Preis-Daten laden (für ALLE Zeiträume)
# ===========================
assets = portfolios.columns.tolist()
if not assets:
    raise ValueError("❌ Keine Assets gefunden für Preis-Daten. Portfolio-Generierung prüfen.")

ticker_mapping = {"BRK-B": "BRK.B"}
assets = [ticker_mapping.get(asset, asset) for asset in assets]

price_data_list = []

for start_date, end_date in date_ranges:
    print(f"📈 Lade historische Preis-Daten via yahooquery für den Zeitraum {start_date} bis {end_date}...")
    tickers = Ticker(assets)
    price_data_period = tickers.history(start=start_date, end=end_date)
    
    if price_data_period.empty:
        print(f"⚠️ Keine Daten für Zeitraum {start_date} bis {end_date} gefunden.")
        continue

    price_data_period = price_data_period['adjclose'].unstack(level=0)
    price_data_list.append(price_data_period)

# ===========================
# 8. Preis-Daten zusammenführen
# ===========================
if not price_data_list:
    raise ValueError("❌ Keine gültigen Preis-Daten für die angegebenen Zeiträume gefunden.")

price_data = pd.concat(price_data_list).sort_index().drop_duplicates()
price_data.to_csv('data/processed/price_data.csv')
print("✅ Preis-Daten erfolgreich gespeichert.")

# ===========================
# 9. Gemeinsame Assets prüfen
# ===========================
common_assets = price_data.columns.intersection(portfolios.columns)
price_data = price_data[common_assets]
portfolios = portfolios[common_assets].copy()
print(f"✅ Gemeinsame Assets für Simulation: {list(common_assets)}")

# ===========================
# 10. Monte Carlo Simulation
# ===========================
simulation_results_df, asset_averages = run_monte_carlo(price_data, portfolios)
print("✅ Monte Carlo Simulation abgeschlossen.")

# ===========================
# 11. Simulationsergebnisse analysieren
# ===========================
simulation_results_df, best_portfolio_id = analyze_simulation_results(simulation_results_df, portfolios)

# ===========================
# 12. Visualisierung
# ===========================
plot_monte_carlo(simulation_results_df, best_portfolio_id)
plot_portfolio_allocation(portfolios.loc[best_portfolio_id])
plot_asset_averages(asset_averages)

print("\n🎉 Simulation und Analyse abgeschlossen.")
