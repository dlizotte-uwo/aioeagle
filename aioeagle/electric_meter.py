from .util import xmltodict_ensure_list, create_command
from .zigbee_device import ZigbeeDevice

class ElectricMeter(ZigbeeDevice):
    """Represent an electric meter.

    {'ConnectionStatus': 'Connected',
      'HardwareAddress': '0x00abcd123',
      'LastContact': '0x611d885a',
      'Manufacturer': 'Generic',
      'ModelId': 'electric_meter',
      'Name': 'Power Meter',
      'NetworkAddress': '0x0000',
      'Protocol': 'Zigbee'}
    """

    # Bug in the API is causing CurrentSummationDelivered not
    # to be returned. So just fetch all (default behavior)
    ENERGY_AND_POWER_VARIABLES = [
        "zigbee:CurrentSummationDelivered",
        "zigbee:CurrentSummationReceived",
        "zigbee:InstantaneousDemand",
    ]

    @classmethod
    def create_instance(cls, hub, hardware_address):
        """Create a new electric meter."""
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
                    "Name": "Main",
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
            for variable in component["Variables"]["Variable"]:
                result[variable["Name"]] = variable

        return result

    def __repr__(self) -> str:
        return f"<ZigbeeDevice {self.details.get('Name', '')}>"

    def __repr__(self) -> str:
        return f"<ElectricMeter {self.details.get('Name', '')}>"
