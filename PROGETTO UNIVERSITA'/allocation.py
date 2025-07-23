import numpy as np
import pandas as pd
from scipy.optimize import minimize

def optimize_allocation(mu_selected, Sigma_selected, budget=20000):
    """Optimize asset allocation to maximize Sharpe Ratio."""
    num_selected_assets = len(mu_selected)
    def negative_sharpe_ratio(weights):
        portfolio_return = np.sum(mu_selected * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(Sigma_selected, weights)))
        risk_free_rate = 0.02
        sharpe = (portfolio_return - risk_free_rate) / portfolio_volatility
        return -sharpe
    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
    bounds = tuple((0, 1) for _ in range(num_selected_assets))
    initial_weights = np.array(num_selected_assets * [1. / num_selected_assets,])
    optimization_result = minimize(fun=negative_sharpe_ratio,
                                   x0=initial_weights,
                                   method='SLSQP',
                                   bounds=bounds,
                                   constraints=constraints)
    optimal_weights = optimization_result.x
    allocation_df = pd.DataFrame(data={'Ticker': mu_selected.index, 'Optimal Allocation': optimal_weights})
    allocation_df['Optimal Allocation'] = allocation_df['Optimal Allocation'].map('{:.2%}'.format)
    allocation_df['Investment ($)'] = pd.Series(optimal_weights * budget).map('${:,.2f}'.format)
    return allocation_df, optimal_weights 