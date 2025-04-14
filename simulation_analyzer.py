import pandas as pd
import numpy as np

def analyze_simulation_results(simulation_results_df, portfolios):
    """
    Analysiert die Monte-Carlo-Simulationsergebnisse auf Portfolio-Ebene.
    Speichert vollständige Ergebnisse und Top-Rankings als CSV.
    """

    print("🔍 Starte Analyse der Simulationsergebnisse...")

    # Vorbereitung: Records für Analyse
    records = []

    for idx, row in simulation_results_df.iterrows():
        path = row['simulation_path']

        # Die Pfade sind als String gespeichert -> konvertieren
        if isinstance(path, str):
            path = eval(path)

        returns = pd.Series(path).pct_change().dropna()

        total_return = (path[-1] - path[0]) / path[0]
        volatility = returns.std()
        max_drawdown = ((pd.Series(path) / pd.Series(path).cummax()) - 1).min()
        sharpe_ratio = returns.mean() / (returns.std() + 1e-9)  # Sicherheit gegen Division durch Null

        records.append({
            'portfolio_id': row['portfolio_id'],
            'simulation_id': row['simulation_id'],
            'total_return': total_return,
            'volatility': volatility,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio
        })

    df = pd.DataFrame(records)

    # 🧩 Finaler Score basierend auf deinen Vorgaben
    df['score_total_return'] = df['total_return']
    df['score_sharpe_ratio'] = df['sharpe_ratio']

    df['final_score'] = (
        0.90 * df['score_total_return'] +
        0.10 * df['score_sharpe_ratio']
    )

    # ✅ Speichern aller Simulationsergebnisse
    df.to_csv('data/processed/simulation_results.csv', index=False)
    print("✅ Simulationsergebnisse gespeichert: data/processed/simulation_results.csv")

    # 🏆 Top 5 Portfolios speichern
    top5 = df.groupby('portfolio_id').mean(numeric_only=True).sort_values('final_score', ascending=False).head(5)
    top5.to_csv('data/processed/top_rankings.csv', index=True)
    print("🏆 Top 5 Portfolios gespeichert unter: data/processed/top_rankings.csv")

    # Hole die beste Portfolio ID für Visualisierung später
    best_portfolio_id = int(top5.index[0])

    print(f"🏆 Bestes Portfolio: ID {best_portfolio_id}")

    return df, best_portfolio_id
