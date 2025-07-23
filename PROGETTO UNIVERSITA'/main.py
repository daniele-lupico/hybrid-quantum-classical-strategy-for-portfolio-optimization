import numpy as np
import random

random.seed(42)
np.random.seed(42)

from data_download import download_and_clean_data, TICKERS
from financial_metrics import calculate_financial_metrics, plot_covariance_heatmap
from qubo_selection import build_qubo, solve_qubo
from allocation import optimize_allocation
from backtest import run_backtest

if __name__ == "__main__":
    # 1. Download and clean data
    prices_df, tickers, start_date, end_date = download_and_clean_data(TICKERS)

    # 2. Calculate financial metrics
    returns_df, mu, Sigma = calculate_financial_metrics(prices_df)
    plot_covariance_heatmap(Sigma)

    # 3. QUBO selection
    Q = build_qubo(mu, Sigma, K=10, gamma=0.5)
    selected_tickers = solve_qubo(Q, tickers, K=10)
    print(f"\nTickers selected by QUBO: {selected_tickers}")

    # 4. Optimal allocation
    mu_selected = mu[selected_tickers]
    Sigma_selected = Sigma.loc[selected_tickers, selected_tickers]
    allocation_df, optimal_weights = optimize_allocation(mu_selected, Sigma_selected, budget=20000)
    print("\n--- Optimal Allocation ---")
    print(allocation_df)

    # 5. Backtest
    run_backtest(returns_df, selected_tickers, optimal_weights, start_date, end_date, budget=20000) 