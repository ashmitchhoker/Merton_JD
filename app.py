from flask import Flask, render_template
import numpy as np

app = Flask(__name__)

# Your jump_diffusion_monte_carlo function goes here

@app.route('/')
def index():
    S0 = 100.0  # Initial stock price
    K = 100.0   # Strike price
    T = 1.0    # Time to maturity
    r = 0.05   # Risk-free interest rate
    sigma = 0.2  # Volatility
    lambd = 0.2  # Jump intensity
    jumps = 1  # Number of jumps in the model
    n_simulations = 1000 # Number of Monte Carlo simulations
    n_steps = 100  # Number of time steps

    # Generate option prices for 30 days
    asset_prices = np.random.uniform(95, 105, size=(30,))
    option_prices = []

    for asset_price in asset_prices:
        option_price = jump_diffusion_monte_carlo(asset_price, K, T, r, sigma, lambd, jumps, n_simulations, n_steps)
        option_prices.append(option_price)

    return render_template('index.html', option_prices=option_prices)

if __name__ == '__main__':
    app.run(debug=True)
