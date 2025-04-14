import numpy as np
import pandas as pd

def run_monte_carlo(prices, portfolio_allocations, num_simulations=30, num_days=252):
    print(f"🧩 Starte Monte Carlo Simulation für {num_simulations} Simulationen pro Portfolio.")

    # ✅ Safety alignment: nur die gemeinsamen Assets verwenden
    common_assets = prices.columns.intersection(portfolio_allocations.columns)
    prices = prices[common_assets]
    portfolio_allocations = portfolio_allocations[common_assets]

    print(f"🧩 Gemeinsame Assets in Simulation: {list(common_assets)}")

    # Log-Returns berechnen für Bootstrap
    log_returns = np.log(prices / prices.shift(1)).dropna()

    # 🧩 Zwischenspeichern: Einzelpfade pro Asset
    asset_paths = {}

    for asset in common_assets:
        asset_returns = log_returns[asset].dropna()

        # Sicherstellen, dass genug Daten vorhanden sind
        if asset_returns.empty:
            print(f"⚠️ Keine Daten für Asset: {asset}")
            continue

        simulations = []

        for _ in range(num_simulations):
            sampled_returns = np.random.choice(asset_returns, size=num_days, replace=True)
            path = [1]
            for ret in sampled_returns:
                path.append(path[-1] * np.exp(ret))
            simulations.append(path)

        asset_paths[asset] = simulations

    # ✅ Durchschnittspfad je Asset berechnen
    asset_averages = {}
    for asset, paths in asset_paths.items():
        asset_averages[asset] = np.mean(paths, axis=0)

    # ✅ Zwischenspeichern der Durchschnittspfade
    pd.DataFrame(asset_averages).to_csv('data/processed/asset_average_paths.csv', index=False)
    print("✅ Durchschnittliche Asset-Pfade gespeichert: data/processed/asset_average_paths.csv")

    # 🧩 Jetzt auf Portfolio-Ebene aggregieren
    portfolio_simulations = []

    for portfolio_id, allocation in portfolio_allocations.iterrows():
        allocation = allocation.fillna(0).values  # Sicherheit

        # Portfolio Average Path
        weighted_paths = np.zeros(num_days + 1)

        for idx, asset in enumerate(common_assets):
            weighted_paths += asset_averages[asset] * allocation[idx]

        for sim in range(num_simulations):
            portfolio_simulations.append({
                'portfolio_id': portfolio_id,
                'simulation_id': sim,
                'simulation_path': weighted_paths.tolist()  # In Liste konvertieren für spätere Speicherung
            })

    # ✅ Ergebnisse als DataFrame speichern
    results_df = pd.DataFrame(portfolio_simulations)
    results_df.to_csv('data/processed/monte_carlo_results.csv', index=False)
    print("✅ Monte Carlo Portfolio-Ergebnisse gespeichert: data/processed/monte_carlo_results.csv")

    return results_df, asset_averages
