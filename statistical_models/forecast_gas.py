import os    
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from datetime import datetime

from matplotlib import pyplot 
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
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
prices_df = pd.DataFrame({'price': prices}, index=dates)

# Seasonal decompose - unhash to see plot
result = seasonal_decompose(prices_df, period=len(prices_df)//2)
# result.plot()
# pyplot.show()


# Analysis of time series
ad_fuller_result = adfuller(prices_df)
print(f'ADF Statistic: {ad_fuller_result[0]}')
print(f'p-value: {ad_fuller_result[1]}')

# ACF - time series has high level of autocorrelation
# plot_acf(prices_df)
# pyplot.show()

# Make my time serie stationary
prev_pices = prices_df.shift()
differenced_prices = prices_df - prev_pices
differenced_prices = differenced_prices.fillna(0)

# Against adfuller analysis to check stationarity 
"""As we can see, the p-value is now very small so job has been done"""
ad_fuller_result = adfuller(differenced_prices)
print(f'ADF Statistic: {ad_fuller_result[0]}')
print(f'p-value: {ad_fuller_result[1]}')


train = prices_df[:442]
test = prices_df[442:]

sarima = SARIMAX(train,
                order=(1,1,2),
                seasonal_order=(1,1,0,12))
sarima.fit()
predictions = sarima.predict(100)
pyplot.plot(predictions)
pyplot.show()