import os    
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import csv
import pandas as pd
import matplotlib.pyplot as plt

from sktime import *

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

# represent our time serie
plt.plot(prices.index, prices['price'])
plt.show()
