import requests
import csv


class PricesOfEnergy:

    def __init__(self, url_to_electric: str, gas_file: str):
        self.url_to_electric = url_to_electric
        self.gas_file = gas_file

    def download_electricity_prices(self) -> list[str]:
        prices_file = requests.get(self.url_to_electric)
        decoded_prices_file = prices_file.content.decode('utf-8')
        csv_prices = csv.reader(decoded_prices_file.splitlines(), delimiter=';')
        return list(csv_prices)

    def download_gas_prices(self) -> list[str]:
        prices_file = self.gas_file
        with open(prices_file) as f:
            csv_prices = csv.reader(f)
            return list(csv_prices)


