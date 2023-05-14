import os    
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from datetime import datetime

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller, kpss
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
import csv
import pandas as pd

"""
This module of project is used to predict future values of gas-prices on stock market. I used SARIMAX model.
This is ready script and you can run full-analysis, but you also must download 'ceny_gazu.csv' file. 
"""

# Open file with gas prices 
with open('ceny_gazu.csv') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    prices, dates = [], []
    for row in reader:
        row = row[0].split(";")
        price = row[1].replace("$", ".")
        date = row[0].replace('/', '-')
        
        prices.append(float(price))
        date = datetime.strptime(date, "%m-%d-%Y")
        dates.append(date)

# Create data frame object with structure - date:gas_price
prices_df = pd.DataFrame({'price': prices})

# Seasonal decompose - unhash to see plot
result_decompose = seasonal_decompose(prices_df, period=len(prices_df)//2)
seasonal = result_decompose.seasonal

# Analysis of time serie KPSS and ADF tests - parameter d, and DHF test for parameter D
adfuller_result = adfuller(prices_df)
print(f'p-value for non-differenced serie: {adfuller_result[1]}')

kpss_result = kpss(prices_df)
print(f"kpss_result for non-differenced serie: {kpss_result}")

dhf_result = adfuller(prices_df, regression='ct', autolag=None)
print(f"p-value for not-differnced dhf test {dhf_result[1]}")

# Differencig of time serie
differenced_prices = prices_df.diff()
differenced_prices = differenced_prices.fillna(0)

# plot autocorellation of differenced prices(unhash to see)
# plot_acf(differenced_prices)
# plt.show()

# Analysis of the dyffirenced time serie - as we can see time serie after one differencing is stationary
differenced_adfuller = adfuller(differenced_prices)
print(f'p-value for differencd one time serie - adfuller: {differenced_adfuller[1]}')

differenced_kpss = kpss(differenced_prices)
print(f"kpss result for differenced one time serie {differenced_kpss}")

differenced_dhf = adfuller(differenced_prices, regression='ct', autolag=None)
print(f"p-value for differnced one time serie - dhf test {differenced_dhf[1]}")

# auto - arima
result_sarima = auto_arima(differenced_prices, seasonal=True, m=5, suppress_warnings=True)
print(result_sarima)

# SARIMA model building
model = SARIMAX(prices_df, order=(1, 1, 1), seasonal_order=(1, 1, 1, 5))
model_fit = model.fit()
predictions = model_fit.predict(start=0, end=len(prices_df)+100)
