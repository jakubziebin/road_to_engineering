import os    
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt

from sktime.forecasting.model_selection import temporal_train_test_split

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

y_train, y_test = temporal_train_test_split(prices, test_size=52)

# forecasting horizon
fh = np.arange(1, 20)

forecaster = AutoETS()
forecaster.fit(y_train)
prediction = forecaster.predict(fh)


plt.plot(prediction)
plt.show()
