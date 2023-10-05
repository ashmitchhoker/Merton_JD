import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            S0 = float(request.form['S0'])
            K = float(request.form['K'])
            T = float(request.form['T'])
            r = float(request.form['r'])
            sigma = float(request.form['sigma'])
            lambd = float(request.form['lambd'])
            jumps = int(request.form['jumps'])
            n_steps = int(request.form['n_steps'])

            # Set n_simulations to 1 (permanently)
            n_simulations = 100

            option_price = jump_diffusion_monte_carlo(S0, K, T, r, sigma, lambd, jumps, n_simulations, n_steps)

            # Generate a plot (as before)
            #n_days = 30 
            lst = np.random.uniform(S0-10, S0+10, size =(30, ))
            x = []
            for i in range (30):
             x.append(jump_diffusion_monte_carlo(lst[i], K, T, r, sigma, lambd, jumps, n_simulations, n_steps))
            plt.figure(figsize=(10, 6))
            
                
            plt.plot( x)
            plt.xlabel('days')
            plt.ylabel('Option price')
            plt.title('option prices')
            plt.grid(True)

            # Save the plot to a temporary file
            plot_filename = 'static/plot.png'
            plt.savefig(plot_filename, format='png')
            plt.close()

            return render_template('index.html', option_price=option_price, plot_filename=plot_filename, calculation_successful=True)
        except ValueError:
            return render_template('index.html', calculation_successful=False)
    
    return render_template('index.html', calculation_successful=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
