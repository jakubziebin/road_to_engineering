from __future__ import annotations

import requests
import csv


class PricesOfEnergy:
    """
    url_to_electric: "https://www.pse.pl/getcsv/-/export/csv/PL_CENY_RYN_EN/data/{today_date_for_electricity}", you need to 
    insert today date in in YMD format. Gas file actually is in the file of the project.
    """

    def __init__(self, url_to_electric: str, gas_file: str):
        self.url_to_electric = url_to_electric
        self.gas_file = gas_file
    
    def __repr__(self) -> str:
        return f"This class download csv files with prices of gas and electricty"

    def __str__(self) -> str:
        return f"This class download csv files with prices of gas and electricty"
        
    def download_electricity_prices(self) -> list[str]:
        prices_file = requests.get(self.url_to_electric)
        decoded_prices_file = prices_file.content.decode('utf-8')
        csv_prices = csv.reader(decoded_prices_file.splitlines(), delimiter=';')
        return list(csv_prices)

    def get_gas_price(self) -> str:
       actual_gas_price = "293.43"  # zł/MWh
       return actual_gas_price
