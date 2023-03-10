import requests
import csv
"""
url_to_electric: "https://www.pse.pl/getcsv/-/export/csv/PL_CENY_RYN_EN/data/{today_date_for_electricity}", you need to insert 
todays date in in YMD format. Gas file actually is in the file of the project.
"""

class PricesOfEnergy:

    def __init__(self, url_to_electric: str, gas_file: str):
        self.url_to_electric = url_to_electric
        self.gas_file = gas_file
    
    def __repr__(self) -> str:
        return f"This class download csv files with prices of gas and electricty"

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


