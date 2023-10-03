from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Define the route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    # Default parameter values
    default_values = {
        'S0': 100.0,
        'r': 0.05,
        'sigma': 0.2,
        'T': 1.0,
        'lambda_J': 0.1,
        'mu_J': -0.1,
        'sigma_J': 0.2
    }

    if request.method == 'POST':
        # Retrieve user input from the form or use default values if not provided
        S0 = float(request.form.get('S0', default_values['S0']))
        r = float(request.form.get('r', default_values['r']))
        sigma = float(request.form.get('sigma', default_values['sigma']))
        T = float(request.form.get('T', default_values['T']))
        lambda_J = float(request.form.get('lambda_J', default_values['lambda_J']))
        mu_J = float(request.form.get('mu_J', default_values['mu_J']))
        sigma_J = float(request.form.get('sigma_J', default_values['sigma_J']))

        # Perform the Merton Jump Diffusion simulation
        # (Insert your simulation code here)

        # Generate a simple plot (you can customize this)
        x = np.linspace(0, T, 100)
        y = S0 * np.exp((r - lambda_J * (mu_J + 0.5 * sigma_J ** 2)) * x + sigma * np.sqrt(x) * np.random.normal(size=100))

        plt.plot(x, y)
        plt.xlabel('Time')
        plt.ylabel('Stock Price')
        plt.title('Merton Jump Diffusion Simulation')
        plt.grid(True)

        # Save the plot to a BytesIO object and encode it as base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plot_data = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        return render_template('index.html', plot_filename=f'data:image/png;base64,{plot_data}', default_values=default_values)

    return render_template('index.html', default_values=default_values)

if __name__ == '__main__':
    app.run(debug=True)
