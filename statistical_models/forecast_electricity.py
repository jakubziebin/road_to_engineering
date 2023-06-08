from __future__ import annotations
import os    
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import pandas as pd
import csv


with open('ceny_energii_elektrycznej.csv') as f:
        reader = csv.reader(f)
        header = next(reader)
    
        prices = []
        for row in reader:
            row = row[0].split(";")
            if row[1] == '12':
                if "1ďż˝" in row[2]:
                    price = row[2].split("1ďż˝")
                    price = f"{price[0]}{price[1]}"
                else:
                    price = row[2]
                prices.append(float(price))


prices_df = pd.DataFrame({'price': prices})
print(prices_df)

