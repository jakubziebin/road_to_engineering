from __future__ import annotations


def get_price_of_electricity(hour_to_find: str, prices: list[str]) -> float:
    """This function is searching a price of electricity for an hour that you need"""
    for row in prices:
        if row[1] == hour_to_find:
            row[2] = row[2].replace(",", ".")
            return float(row[2])


def get_price_of_gas(price: str) -> float:
    """Cause requirements of project has been change, this funtion just convert string to float :("""
    return float(price)
