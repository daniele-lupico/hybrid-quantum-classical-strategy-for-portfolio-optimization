import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os

def calculate_performance_metrics(cumulative_returns, daily_returns, risk_free_rate_daily=0):
    """Calculate total return, CAGR, max drawdown, and Sharpe ratio."""
    total_return = (cumulative_returns.iloc[-1] - 1)
    num_years = len(cumulative_returns) / 252
    cagr = (cumulative_returns.iloc[-1])**(1/num_years) - 1
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) / running_max
    max_drawdown = drawdown.min()
    excess_returns = daily_returns - risk_free_rate_daily
    sharpe_ratio = (excess_returns.mean() / excess_returns.std()) * (252 ** 0.5)
    return total_return, cagr, max_drawdown, sharpe_ratio, drawdown

def run_backtest(returns_df, selected_tickers, optimal_weights, start_date, end_date, budget=20000):
    """Run backtest and compare with QQQ benchmark. Save drawdown plot in images folder."""
    # Ensure images directory exists
    os.makedirs('images', exist_ok=True)

    final_weights = optimal_weights
    returns_selected = returns_df[selected_tickers]
    portfolio_daily_returns = returns_selected.dot(final_weights)
    portfolio_cumulative_returns = (1 + portfolio_daily_returns).cumprod()
    # Benchmark QQQ
    qqq_prices = yf.download('QQQ', start=start_date, end=end_date)['Close']
    qqq_daily_returns = qqq_prices.pct_change().dropna()
    qqq_daily_returns = qqq_daily_returns.reindex(portfolio_cumulative_returns.index).ffill()
    qqq_cumulative_returns = (1 + qqq_daily_returns).cumprod()
    # Performance metrics
    risk_free_daily = 0.03 / 252
    p_total_return, p_cagr, p_max_drawdown, p_sharpe, p_drawdown = calculate_performance_metrics(
        portfolio_cumulative_returns, portfolio_daily_returns, risk_free_rate_daily=risk_free_daily)
    q_total_return, q_cagr, q_max_drawdown, q_sharpe, q_drawdown = calculate_performance_metrics(
        qqq_cumulative_returns, qqq_daily_returns, risk_free_rate_daily=risk_free_daily)
    # Ensure drawdowns are 1D
    p_drawdown = pd.Series(p_drawdown.squeeze(), index=portfolio_cumulative_returns.index)
    q_drawdown = pd.Series(q_drawdown.squeeze(), index=portfolio_cumulative_returns.index)
    # Plot: Drawdown comparison
    drawdown_df = pd.DataFrame({
        'Optimized Portfolio Drawdown': p_drawdown,
        'Benchmark (QQQ) Drawdown': q_drawdown
    })
    ax = drawdown_df.plot(figsize=(14, 7), title='Drawdown Comparison: Optimized Portfolio vs. Benchmark (QQQ)')
    plt.ylabel('Drawdown')
    plt.xlabel('Date')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('images/drawdown_comparison.png')
    plt.close()
    # Print results
    print("\n--- BACKTEST RESULTS (Buy & Hold) ---")
    print(f"Total Return of Optimized Portfolio: {p_total_return:.2%}")
    print(f"Annualized Return (CAGR) of Portfolio: {p_cagr:.2%}")
    print(f"Max Drawdown of Portfolio: {p_max_drawdown:.2%}")
    print(f"Sharpe Ratio of Portfolio: {p_sharpe:.2f}")
    print("-" * 50)
    print(f"Total Return of Benchmark (QQQ): {q_total_return.item():.2%}")
    print(f"Annualized Return (CAGR) of Benchmark (QQQ): {q_cagr.item():.2%}")
    print(f"Max Drawdown of Benchmark (QQQ): {q_max_drawdown.item():.2%}")
    print(f"Sharpe Ratio of Benchmark (QQQ): {q_sharpe.item():.2f}")
    print("-" * 50) 