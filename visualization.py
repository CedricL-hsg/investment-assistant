import matplotlib.pyplot as plt
import pandas as pd
import ast

def plot_monte_carlo(simulation_results_df, best_portfolio_id):
    # ✅ Simulation Paths laden
    simulation_paths = pd.read_csv('data/processed/monte_carlo_results.csv')
    print("Spalten in monte_carlo_results.csv:", simulation_paths.columns.tolist())  # Debugging

    # ✅ Filtern auf bestes Portfolio
    best_paths = simulation_paths[simulation_paths['portfolio_id'] == best_portfolio_id]

    if best_paths.empty:
        print(f"⚠️ Keine Simulationen gefunden für Portfolio ID {best_portfolio_id}.")
        return

    plt.figure(figsize=(12, 6))

    # ✅ Alle Pfade zeichnen
    for _, row in best_paths.iterrows():
        sim_path = ast.literal_eval(row['simulation_path'])  # <- hier angepasst!
        plt.plot(sim_path, alpha=0.2, color='blue')

    # ✅ Durchschnittspfad zusätzlich in Orange
    all_paths = [ast.literal_eval(row['simulation_path']) for _, row in best_paths.iterrows()]
    average_path = [sum(x) / len(x) for x in zip(*all_paths)]
    plt.plot(average_path, color='orange', linewidth=2, label='Durchschnittspfad')

    plt.title('Monte Carlo Simulation - Bestes Portfolio')
    plt.xlabel('Tage')
    plt.ylabel('Portfolio Wert')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_portfolio_allocation(portfolio):
    portfolio = portfolio[portfolio > 0]
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        portfolio,
        labels=portfolio.index,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.85
    )
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)

    for text in texts + autotexts:
        text.set_fontsize(10)

    plt.title('Portfolio Allokation', fontsize=14)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def plot_asset_averages(asset_averages):
    plt.figure(figsize=(12, 6))
    for asset, path in asset_averages.items():
        plt.plot(path, label=asset)
    plt.title('Durchschnittliche Asset-Pfade')
    plt.xlabel('Tage')
    plt.ylabel('Asset Wert')
    plt.legend()
    plt.grid(True)
    plt.show()
