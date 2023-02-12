"""
Gas prices is given from date x to date y. Gas date parameter have to be input in "%d.%m.%Y" format.
Hour to find, just put number, but in 24 hour format.
"""

def get_price_of_electricity(hour_to_find: str, prices: list[str]) -> float:
    for row in prices:
        if row[1] == hour_to_find:
            row[2] = row[2].replace(",", ".")
            return float(row[2])


def get_price_of_gas(gas_date: str, prices: list[str]) -> float:
    for row in prices:
        print(row)
        if row[0] == gas_date:
            row[3] = row[3].replace(",", ".")
            return float(row[3])
    
