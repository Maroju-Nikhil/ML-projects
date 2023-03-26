from flask import Flask, render_template
import pandas as pd

car = pd.read_csv('cleaned_car.csv')
app = Flask(__name__)


@app.route('/')
def index():
    car_companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    years = sorted(car['year'].unique(), reverse=True)
    fuel_type = car['fuel_type'].unique()
    data = {
        "companies": car_companies,
        "models": car_models,
        "years": years,
        "fuel_types": fuel_type,
    }
    return render_template('index.html', data = data)


if __name__ == "__main__":
    app.run(debug=True)