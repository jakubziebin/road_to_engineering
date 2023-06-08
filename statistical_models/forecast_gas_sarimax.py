from __future__ import annotations
import os    
os.chdir(os.path.dirname(os.path.abspath(__file__)))


import matplotlib.pyplot as plt
import pandas as pd
import csv

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.statespace.sarimax import SARIMAX

"""
This module of project is used to predict future values of gas-prices on stock market. I used SARIMAX model.
This is ready script and you can run full-analysis, but you also must download 'ceny_gazu.csv' file. 
"""


def read_prices_from_csv() -> list[float]:
    """This function is used to read previous prices of gas 
       from stock market(csv file is included in package)
    """
    with open('ceny_gazu.csv') as f:
        reader = csv.reader(f)
        header = next(reader)
    
        prices = []
        for row in reader:
            row = row[0].split(";")
            price = row[1].replace("$", ".")
            prices.append(float(price))
        return prices


def analise_time_serie(prices_df: pd.DataFrame) -> None:
    """
    This function is making full analise of time serie, plots pacf and acf, make kpss and adfuller test on 
    original and differnced time serie   
    """

    result_decompose = seasonal_decompose(prices_df, period=len(prices_df)//2)
    seasonal = result_decompose.seasonal # i get just seasonal part to analise

    # Analysis of time serie -> KPSS and ADF tests - parameter d, and DHF test for parameter D
    adfuller_result = adfuller(prices_df)
    print(f'p-value for non-differenced serie: {adfuller_result[1]}')

    kpss_result = kpss(prices_df)
    print(f"kpss_result for non-differenced serie: {kpss_result}")

    dhf_result = adfuller(prices_df, regression='ct', autolag=None)
    print(f"p-value for not-differnced dhf test {dhf_result[1]}")

    differenced_prices = prices_df.diff() # time serie need to be differenced, cause it was not stationary
    differenced_prices = differenced_prices.fillna(0)

    # Analysis of the dyffirenced time serie - as we can see time serie after one differencing is stationary
    differenced_adfuller = adfuller(differenced_prices)
    print(f'p-value for differencd one time serie - adfuller: {differenced_adfuller[1]}')

    differenced_kpss = kpss(differenced_prices)
    print(f"kpss result for differenced one time serie {differenced_kpss}")

    differenced_dhf = adfuller(differenced_prices, regression='ct', autolag=None)
    print(f"p-value for differnced one time serie - dhf test {differenced_dhf[1]}")

    plot_acf(differenced_prices)
    plt.show()

    plot_pacf(differenced_prices)
    plt.show()


def create_model(prices: pd.DataFrame, horizont: int) -> pd.DataFrame:
    model = SARIMAX(prices, order=(1, 1, 1), seasonal_order=(1, 1, 1, 5))
    model_fit = model.fit()
    predictions = model_fit.predict(start=0, end=len(prices)+horizont)
    return predictions[6:]


if __name__ == "__main__":
    prices_df = pd.DataFrame({'price': read_prices_from_csv()})
    analise_time_serie(prices_df)

    model = create_model(prices_df,  3-)

    plt.plot(model)
    plt.plot(prices_df)
    plt.title("Porównanie przebiegów, prognoza na miesiąc")
    plt.show()
