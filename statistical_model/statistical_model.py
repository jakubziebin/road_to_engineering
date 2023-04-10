import os    
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt

from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.forecasting.theta import ThetaForecaster

# Read values from csv file
with open('ceny_gazu.csv') as f:
    reader = csv.reader(f)
    header = next(reader)

    prices = []
    for price in reader:
        price = price[0].replace(";", "")
        prices.append(float(price))

# create data frame object
prices = pd.DataFrame({'price': prices})


# represent our time series
#plt.plot(prices.index, prices['price'])
#plt.show()

gas_train, gas_test = temporal_train_test_split(prices)

fh = np.arange(1, len(gas_test) + 1)  # forecasting horizon
forecaster = ThetaForecaster(sp=12)  # monthly seasonal periodicity
forecaster.fit(gas_train)

y_pred = forecaster.predict(fh)

plt.plot(gas_test)
plt.show()