from opcua import Server

from time import sleep
"""
    This project use to find cheaper way to heat a water. Choose is between heaters which use gas and electricity.
    It is very comfortable situasion with electricity, cause in Poland we have available site, which shows everyday
    electricity prices for every hour. Worse situation is with gas. Our government organisation give us information 
    once by 6 months about it. It definitely not include dynamic of changes gas prices on global markets. 
    I decided to fix it with machine learning model, which would be forecast prices of gas in Poland.
"""

server = Server()
server.set_endpoint("opc.tcp://localhost:4841")
namespace = server.register_namespace("Prices_of_Energy_and_Source_Choose")

objects = server.get_objects_node()
prices_and_choose = objects.add_object(namespace, "PoE")

price_of_gas = prices_and_choose.add_variable(namespace, "price_of_gas", 11.1)
price_of_electricity = prices_and_choose.add_variable(namespace, "price_of_electricity", 11.1)
use_electricity = prices_and_choose.add_variable(namespace, "price_of_electricity", False)
use_gas = prices_and_choose.add_variable(namespace, "price_of_electricity", False)

all_variables = ("price_of_gas", "price_of_electricity", "use_electricity", "use_gas")
for variable in all_variables:
    eval(f"{variable}.set_writable()")

server.start()
print("Server start")
while True:
    print("Server is still here")
    use_gas.set_value(True)
    use_electricity.set_value(True)
    price_of_gas.set_value(1000.1)
    price_of_electricity.set_value(1000.1)
    print(price_of_electricity.get_value())
    sleep(20)


