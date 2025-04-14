import pandas as pd
import numpy as np

def load_asset_allocation():
    return pd.read_csv('data/processed/asset_allocation.csv')

def load_asset_list():
    return pd.read_csv('data/processed/asset_list.csv')

def generate_portfolios(asset_allocation, assets_by_class, num_portfolios=1000, min_weight=0.025, max_weight=0.3):
    portfolios = []

    for _ in range(num_portfolios):
        portfolio = {}

        for asset_class, target_weight in asset_allocation.items():
            assets = assets_by_class.get(asset_class, [])
            if not assets or target_weight == 0:
                continue

            np.random.shuffle(assets)  # Einmal durchmischen für Vielfalt
            assigned_weight = 0
            asset_weights = {asset: 0 for asset in assets}

            while assigned_weight < target_weight / 100:
                for asset in assets:
                    if assigned_weight >= target_weight / 100:
                        break

                    remaining_weight = (target_weight / 100) - assigned_weight
                    max_assignable = min(max_weight, remaining_weight)

                    if max_assignable < min_weight:
                        weight = remaining_weight
                    else:
                        weight = np.random.uniform(min_weight, max_assignable)

                    asset_weights[asset] += weight
                    assigned_weight += weight

            # Alle Asset-Gewichte zur Portfolio-Zusammenstellung hinzufügen
            portfolio.update(asset_weights)

        portfolios.append(portfolio)

    df_portfolios = pd.DataFrame(portfolios).fillna(0)
    df_portfolios.to_csv('data/processed/generated_portfolios.csv', index=False)

    print("✅ Portfolios als CSV gespeichert unter data/processed/generated_portfolios.csv")

    return df_portfolios
