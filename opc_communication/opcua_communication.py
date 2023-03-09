from opcua import Client

def read_value(node_id):
    client_node = client.get_node(node_id)
    client_node_value = client_node.get_value()
    print(client_node_value)


if __name__ == "__main__":
    # Connect to opc ua server implemented in Tia Portal
    client = Client('opc.tcp://192.168.1.10:4840')
    client.connect()

    variables_in_plc = ("PriceOfElectricity", "PriceOfGas", "UseGas", "UseElectricity")

    read_value('ns=3;s="OpcuaPythonTransfer"."PriceOfElectricity"')


