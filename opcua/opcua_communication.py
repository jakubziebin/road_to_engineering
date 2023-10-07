from __future__ import annotations
import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from datetime import datetime, date
from typing import TypeVar
from time import sleep

from opcua import Client, ua

from prices_of_energy import preparing_datas_to_send
from prices_of_energy import PricesOfEnergy
from database.db_functions import connect_to_db, put_value_into_db


Node = TypeVar('Node')

def read_value(node_id: str) -> Node:
    client_node = client.get_node(node_id)
    client_node_value = client_node.get_value()
    return client_node_value


def write_real_value(node_id: str, value: float) -> None:
    client_node = client.get_node(node_id)
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Float))
    client_node.set_value(client_node_dv)


def write_bool_value(node_id: str, value: bool) -> None:
    client_node = client.get_node(node_id)
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Boolean))
    client_node.set_value(client_node_dv)


QUERY_TO_DB = """INSERT INTO TABLE (place_for_value) VALUES ((%s))""" 

if __name__ == "__main__":
    DATA_BLOCK_FOR_OPCUA_COMMUNICATION = "OpcuaPythonTransfer"
    VARIABLES_IN_PLC = ("PriceOfElectricity", "PriceOfGas", "Tin", "Flow", "Tsp")

    today_date_for_electricity = str(date.today().strftime("%Y%m%d"))
    url_to_electricity = f"https://www.pse.pl/getcsv/-/export/csv/PL_CENY_RYN_EN/data/{today_date_for_electricity}"
    gas_file = "gas_prices.csv" 
    prices = PricesOfEnergy(url_to_electricity, gas_file)
    electricity_prices = prices.download_electricity_prices()

    # Connect to opc ua server implemented in Tia Portal
    client = Client('opc.tcp://192.168.1.10:4840')
    client.connect()

    while True:
        actual_hour = str(datetime.now().hour)
        electricity_price = preparing_datas_to_send.get_price_of_electricity(actual_hour, electricity_prices)
        
        gas_price = preparing_datas_to_send.get_price_of_gas(prices.get_gas_price())
        t_set_point = 71.0

        write_real_value(f"""ns=3;s="OpcuaPythonTransfer".{VARIABLES_IN_PLC[0]}""", electricity_price)
        write_real_value(f'ns=3;s="OpcuaPythonTransfer".{VARIABLES_IN_PLC[1]}', gas_price)
        write_real_value(f"""ns=3;s="OpcuaPythonTransfer".{VARIABLES_IN_PLC[4]}""", t_set_point)

        sleep(10)
