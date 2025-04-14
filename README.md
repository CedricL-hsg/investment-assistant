# 📊 Portfolio Simulator with Macro Regime Classification & Monte Carlo Simulation

## 🎯 Project Overview

This project is a dynamic portfolio simulator designed to create and evaluate investment strategies based on real-time macroeconomic indicators. It automatically determines the current macroeconomic regime using live data from the FRED API and runs thousands of simulations to help users understand potential portfolio outcomes.

---

## 🚀 Key Features

- 🔗 **Live macro data** via [FRED API](https://fred.stlouisfed.org/)
- 🧠 **Macro regime classification** using a trained KNN model
- 📈 **Generation of 1000 random portfolio allocations** based on user preferences and the current market regime
- 🎲 **50 Monte Carlo simulations per portfolio** (~50,000 simulations total)
- 📊 **Output as interactive plots and CSV files**

---

## 📁 Project Structure

```plaintext
project/
│
├── app.py                  # Main application script
├── requirements.txt        # Dependencies
│
├── src/                    # Source code modules
│   ├── utils.py
│   ├── portfolio_generator.py
│   └── simulation.py
│
├── data/processed/         # Output and reference data
    ├── macro_classification.csv
    ├── asset_allocation.csv
    ├── portfolio_allocations.csv
    └── all_simulation_results.csv

