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

    ENERGY_AND_POWER_VARIABLES = [
        "zigbee:InstantaneousDemand",
        "zigbee:CurrentSummationDelivered",
    ]

    CONTROL_VARIABLE = "zigbee:OnOff"

    @classmethod
    def create_instance(cls, hub, hardware_address):
        """Create a new smart plug."""
        return cls(
            {
                "HardwareAddress": hardware_address,
            },
            hub.make_request,
        )

    def __repr__(self) -> str:
        return f"<SX885ZB {self.details.get('Name', '')}>"
