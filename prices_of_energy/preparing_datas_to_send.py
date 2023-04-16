"""
To find the price of gas that you need put date: {here_will_be_list_of_datas}
Hour to find, just put number, but in 24 hour format.
"""


def get_price_of_electricity(hour_to_find: str, prices: list[str]) -> float:
    """This function is searching a price of electricity for an hour that you need"""
    for row in prices:
        if row[1] == hour_to_find:
            row[2] = row[2].replace(",", ".")
            return float(row[2])


def get_price_of_gas(gas_date: str, prices: list[str]) -> float:
    """This functions is searching a price of gas for an date that you need"""
    for row in prices:
        print(row)
        if row[0] == gas_date:
            row[3] = row[3].replace(",", ".")
            return float(row[3])
    
