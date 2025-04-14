import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from fredapi import Fred

# === FRED API Schlüssel eintragen ===
FRED_API_KEY = 'c2a4db43eecba591aa06b190d9e93c5e'
fred = Fred(api_key=FRED_API_KEY)

def fetch_live_macro_data():
    indicators = {
        'GDP': 'A191RL1Q225SBEA',
        'Inflation': 'CPALTT01USQ657N',
        'Unemployment': 'UNRATE'
    }

    latest_data = {}
    for name, code in indicators.items():
        try:
            data = fred.get_series_latest_release(code)
            latest_value = data.iloc[-1]
            latest_data[name] = latest_value
        except Exception as e:
            print(f"Fehler beim Abrufen von {name}: {e}")
            latest_data[name] = np.nan

    return pd.DataFrame([latest_data])

def load_macro_classification():
    return pd.read_csv('data/processed/macro_classification.csv')

def classify_market_regime(live_macro_data, macro_classification):
    features = macro_classification.drop(columns=['Regime']).select_dtypes(include=[np.number])
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(features_scaled, macro_classification['Regime'])

    live_features = live_macro_data.select_dtypes(include=[np.number])
    live_scaled = scaler.transform(live_features)

    regime = knn.predict(live_scaled)[0]
    return regime
