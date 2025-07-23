import numpy as np
import pandas as pd
import dimod
from dwave.samplers import SimulatedAnnealingSampler

SEED = 42

def build_qubo(mu, Sigma, K=10, gamma=0.5):
    """Build the QUBO matrix for portfolio selection."""
    num_assets = len(mu)
    P = np.max(np.abs(mu.values)) * 2
    Q = np.zeros((num_assets, num_assets))
    # Off-diagonal terms (interactions between assets)
    for i in range(num_assets):
        for j in range(i + 1, num_assets):
            risk_term = gamma * Sigma.iloc[i, j]
            penalty_term = P
            Q[i, j] = risk_term + penalty_term
            Q[j, i] = Q[i, j]
    # Diagonal terms (individual asset contributions)
    for i in range(num_assets):
        return_term = -mu.iloc[i]
        risk_term = gamma * Sigma.iloc[i, i]
        penalty_term = P * (1 - 2 * K)
        Q[i, i] = return_term + risk_term + penalty_term
    return Q

def solve_qubo(Q, tickers, K=10):
    """Solve the QUBO problem using a simulated annealing sampler with a fixed seed."""
    bqm = dimod.BinaryQuadraticModel.from_qubo(Q, offset=0.0)
    sampler = SimulatedAnnealingSampler()
    sampleset = sampler.sample(bqm, num_reads=1000, seed=SEED)
    best_solution = sampleset.first.sample
    assets = np.array(tickers)
    selected_mask = np.array(list(best_solution.values()), dtype=bool)
    selected_tickers = assets[selected_mask]
    return selected_tickers 