import os    
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from matplotlib import pyplot 
from datetime import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller



import csv
import pandas as pd

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

# create data frame object
prices_df = pd.DataFrame({'price': prices}, index=dates)

# analysis of time series
result = seasonal_decompose(prices_df, period=int(len(prices_df)/2))
"""
adf, pval, usedlag, nobs, crit_vals, icbest =  adfuller(prices_df)
print('ADF test statistic:', adf)
print('ADF p-values:', pval)
print('ADF number of lags used:', usedlag)
print('ADF number of observations:', nobs)
print('ADF critical values:', crit_vals)
print('ADF best information criterion:', icbest)
"""

# Delete trend from my time serie
prev_pices = prices_df.shift()
differenced_prices = prices_df - prev_pices

differenced_prices = differenced_prices.fillna(0)
#differenced_prices.plot()
#pyplot.show()

# against adfuller analysis to check if trend have been deleted. As we can see, it was.
adf, pval, usedlag, nobs, crit_vals, icbest =  adfuller(differenced_prices)
print('ADF against test statistic:', adf)
print('ADF new p-values:', pval)
print('ADF new number of lags used:', usedlag)
print('ADF new number of observations:', nobs)
print('ADF new critical values:', crit_vals)
print('ADF new best information criterion:', icbest)




