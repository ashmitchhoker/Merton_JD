import numpy as np
import matplotlib.pyplot as plt
def jump_diffusion_monte_carlo(S0, K, T, r, sigma, lambd, jumps, n_simulations, n_steps):
    dt = T / n_steps
    discount_factor = np.exp(-r * T)

    option_prices = []
    for _ in range(n_simulations):
        price_path = [S0]
        for _ in range(n_steps):
            Z1 = np.random.normal(0, 1)
            N = np.random.poisson(lambd * dt)
            Z2 = np.random.normal(0, 1, N)
            jump = np.sum(Z2)
            next_price = price_path[-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z1 + jump)
            price_path.append(next_price)

        option_payoff = max(price_path[-1] - K, 0)  # European call option payoff
        option_prices.append(option_payoff)
    option_price = np.mean(option_prices) * discount_factor
    return option_price
# Example usage:
S0 = 100.0  # Initial stock price
K = 100.0   # Strike price
T = 1.0    # Time to maturity
r = 0.05   # Risk-free interest rate
sigma = 0.2  # Volatility
lambd = 0.2  # Jump intensity
jumps = 1  # Number of jumps in the model
n_simulations = 1000 # Number of Monte Carlo simulations
n_steps = 100  # Number of time steps
option_price = jump_diffusion_monte_carlo(S0, K, T, r, sigma, lambd, jumps, n_simulations, n_steps)
print(f"Option Price: {option_price:.4f}")


list = np.random.uniform(95, 105, size = (30,)) #Asset prices in 30 days
m = []
for i in range(30):
  option = jump_diffusion_monte_carlo(list[i], K, T, r, sigma, lambd, jumps, n_simulations, n_steps)
  m.append(option)

plt.plot(m)
plt.title("Estimated option prices")
plt.xlabel("Day of the month")
plt.ylabel("option price")
