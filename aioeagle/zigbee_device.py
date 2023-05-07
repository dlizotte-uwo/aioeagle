from .util import xmltodict_ensure_list, create_command


class ZigbeeDevice:
    """Represent a zigbee device.

    {'ConnectionStatus': 'Connected',
      'HardwareAddress': '0x00abcd123',
      'LastContact': '0x611d885a',
      'Manufacturer': 'SALUS',
      'ModelId': 'S885ZB',
      'Name': 'My Smart Plug',
      'NetworkAddress': '0xABCD',
      'Protocol': 'Zigbee'}
    """
    def __init__(self, details, make_request):
        """Initialize the device."""
        self.details = details
        self.make_request = make_request

    @property
    def is_connected(self) -> bool:
        """Return connection status."""
        return self.details["ConnectionStatus"] == "Connected"

    @property
    def connection_status(self) -> str:
        return self.details["ConnectionStatus"]

    @property
    def hardware_address(self) -> str:
        return self.details["HardwareAddress"]

    @property
    def last_contact(self) -> str:
        return self.details["LastContact"]

    @property
    def manufacturer(self) -> str:
        return self.details["Manufacturer"]

    @property
    def model_id(self) -> str:
        return self.details["ModelId"]

    @property
    def name(self) -> str:
        return self.details["Name"]

    @property
    def network_address(self) -> str:
        return self.details["NetworkAddress"]

    @property
    def protocol(self) -> str:
        return self.details["Protocol"]

    def create_command(self, command, extra_data={}):
        """Create command targeting this device."""
        return create_command(
            command,
            {"DeviceDetails": {"HardwareAddress": self.hardware_address}, **extra_data},
        )

    async def get_device_details(self):
        data = await self.make_request(
            self.create_command(
                "device_details",
            )
        )
        return xmltodict_ensure_list(data["Device"]["Components"], "Component")
