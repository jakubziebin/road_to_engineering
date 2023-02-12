from download_energy_prices import PricesOfEnergy
from datetime import date, datetime

# Parameters to activate functions from this file
today_date_for_electricity = str(date.today().strftime("%Y%m%d"))
today_date_for_gas = str(date.today().strftime("%d.%m.%Y"))
actual_hour = str(datetime.now().hour)

"""
url to electricity need a actual date or date from day, that you want to get information about electricity price.
It have to be in YMD format. Gas prices is given from date x to date y. 
Gas date parameter have to be input in "%d.%m.%Y" format.
"""
url_to_electricity = f"https://www.pse.pl/getcsv/-/export/csv/PL_CENY_RYN_EN/data/{today_date_for_electricity}"
gas_file = "gas_prices.csv"
prices = PricesOfEnergy(url_to_electricity, gas_file)


def get_price_of_electricity_by_date(hour_to_find: str) -> float:
    for row in prices.download_electricity_prices():
        if row[1] == hour_to_find:
            row[2] = row[2].replace(",", ".")
            return float(row[2])


def get_price_of_gas_by_date(gas_date: str) -> float:
    for row in prices.download_gas_prices():
        print(row)
        if row[0] == gas_date:
            row[3] = row[3].replace(",", ".")
            return row[3]