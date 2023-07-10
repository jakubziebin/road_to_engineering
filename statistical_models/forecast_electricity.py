from __future__ import annotations
import os    
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import pandas as pd
import csv

def read_value_from_csv(file_name: str) -> list[float]:
    prices = []
    with open(file_name) as f:
        reader = csv.reader(f)
        header = next(reader)
    
        for row in reader:
            row = row[0].split(";")
            try:
                price = float(row[2])
            except ValueError:
                 print("I did what i could sorry :(") 
                 continue
            prices.append(price)
    return prices


def analise_time_serie(prices: pd.DataFrame) -> None:
    """adfuller test and kpss showed that time serie is stationary, so there is no reason difference it"""
    result_decompose = seasonal_decompose(prices_df, period=len(prices_df)//2)
    seasonal_part = result_decompose.seasonal


    adfuller_result = adfuller(prices_df)
    print(f'p-value for non-differenced serie: {adfuller_result[1]}')

    kpss_result = kpss(prices_df)
    print(f"kpss_result for non-differenced serie: {kpss_result}")

    plot_acf(prices_df)
    plt.show()

    plot_pacf(prices_df)  # parameter p = 2
    plt.show()

    plot_acf(seasonal_part)
    plt.show()

    plot_pacf(seasonal_part)  # parameter P = 2
    plt.show()
    

def create_model(prices: pd.DataFrame, horizont: int) -> pd.DataFrame:
    model = SARIMAX(prices, order=(2, 0, 2), seasonal_order=(2, 0, 2, 24))
    model_fit = model.fit()
    predictions = model_fit.predict(start=0, end=len(prices)+horizont)
    return predictions


if __name__ == "__main__":
    prices = read_value_from_csv('ceny_energii_elektrycznej.csv')
    prices_df = pd.DataFrame({'price': prices})

    test = create_model(prices_df, 1000)
    test.plot()
    plt.plot(prices)
    plt.show()
