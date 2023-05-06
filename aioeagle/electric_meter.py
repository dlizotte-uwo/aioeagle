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
        "zigbee:InstantaneousDemand",
        "zigbee:CurrentSummationDelivered",
        "zigbee:CurrentSummationReceived",
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

    def __repr__(self) -> str:
        return f"<ElectricMeter {self.details.get('Name', '')}>"
