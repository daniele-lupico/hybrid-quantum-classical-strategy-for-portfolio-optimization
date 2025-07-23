import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_financial_metrics(prices_df, trading_days=252):
    """Calculate daily returns, expected annual returns (mu), and annual covariance matrix (Sigma)."""
    returns_df = prices_df.pct_change().dropna()
    mu = returns_df.mean() * trading_days
    mu = mu.round(2)
    Sigma = returns_df.cov() * trading_days
    Sigma = Sigma.round(2)
    return returns_df, mu, Sigma

def plot_covariance_heatmap(Sigma):
    plt.figure(figsize=(12, 10))
    sns.heatmap(Sigma, annot=False, cmap='coolwarm')
    plt.title('Annual Covariance Matrix Heatmap', fontsize=16)
    plt.xlabel('Tickers', fontsize=12)
    plt.ylabel('Tickers', fontsize=12)
    plt.show() 