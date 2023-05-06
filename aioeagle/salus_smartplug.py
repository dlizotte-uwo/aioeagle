from .util import xmltodict_ensure_list, create_command
from .zigbee_device import ZigbeeDevice

class SX885ZB(ZigbeeDevice):
    """Represent a smart plug.

    {'ConnectionStatus': 'Connected',
      'HardwareAddress': '0x00abcd123',
      'LastContact': '0x611d885a',
      'Manufacturer': 'Generic',
      'ModelId': 'SX885ZB',
      'Name': 'My Plug',
      'NetworkAddress': '0xABCD',
      'Protocol': 'Zigbee'}
    """

    # I think these need to be in the order they're stored on the bridge
    ENERGY_AND_POWER_VARIABLES = [
        "zigbee:CurrentSummationDelivered",
        "zigbee:InstantaneousDemand",
    ]

    CONTROL_VARIABLE = [ "zigbee:OnOff", ]

    @classmethod
    def create_instance(cls, hub, hardware_address):
        """Create a new smart plug."""
        return cls(
            {
                "HardwareAddress": hardware_address,
            },
            hub.make_request,
        )
    
    async def get_device_query(self, variables=None):
        """Query data."""
        if variables is None:
            components = {"All": "Y"}
        else:
            components = {
                "Component": {
                    "Name": "SALUS:Receptacle",
                    "Variables": [{"Variable": {"Name": var}} for var in variables],
                }
            }
        data = await self.make_request(
            self.create_command(
                "device_query",
                {"Components": components},
            )
        )
        self.details = data["Device"]["DeviceDetails"]

        result = {}
        for component in xmltodict_ensure_list(
            data["Device"]["Components"], "Component"
        ):
            for variable in xmltodict_ensure_list(component["Variables"],"Variable"):
                result[variable["Name"]] = variable

        return result

    def __repr__(self) -> str:
        return f"<SX885ZB {self.details.get('Name', '')}>"
