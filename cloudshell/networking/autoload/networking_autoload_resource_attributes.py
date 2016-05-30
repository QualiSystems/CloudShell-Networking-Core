from cloudshell.shell.core.driver_context import AutoLoadAttribute


class AttributeContainer(list):
    _DEFAULT_VALUE = ''
    _DEFAULT_VALUES = {}

    def __init__(self, relative_path=None, **kwargs):
        self._default_values = {}
        self.handle_attributes_dict(relative_path, kwargs)

    def append_attribute(self, relative_path, attribute_name, attribute_param):
        if callable(attribute_param):
            attribute_value = attribute_param()
        else:
            attribute_value = attribute_param

        attribute = AutoLoadAttribute(relative_path, attribute_name, attribute_value)
        self.append(attribute)

    def get_attributes_list(self):
        return [getattr(self, attr) for attr in dir(self) if attr.isupper() and not attr.startswith('_')]

    def handle_attributes_dict(self, relative_path, attr_dict):
        final_dict = dict((attr, self._DEFAULT_VALUE) for attr in self.get_attributes_list())
        final_dict.update(self._DEFAULT_VALUES)
        final_dict.update(attr_dict)
        for attr_name, attr_value in final_dict.iteritems():
            self.append_attribute(relative_path, attr_name, attr_value)


class RootAttributes(AttributeContainer):
    VENDOR = 'Vendor'
    SYSTEM_NAME = 'System Name'
    LOCATION = 'Location'
    CONTACT_NAME = 'Contact Name'
    OS_VERSION = 'OS Version'
    MODEL = 'Model'


class ChassisAttributes(AttributeContainer):
    SERIAL_NUMBER = 'Serial Number'
    MODEL = 'Model'


class ModuleAttributes(AttributeContainer):
    SERIAL_NUMBER = 'Serial Number'
    MODEL = 'Model'
    VERSION = 'Version'


class SubModuleAttributes(AttributeContainer):
    SERIAL_NUMBER = 'Serial Number'
    MODEL = 'Model'
    VERSION = 'Version'


class PortAttributes(AttributeContainer):
    PROTOCOL_TYPE = 'Protocol Type'
    PORT_DESCRIPTION = 'Port Description'
    L2_PROTOCOL_TYPE = 'L2 Protocol Type'
    MAC_ADDRESS = 'MAC Address'
    MTU = 'MTU'
    DUPLEX = 'Duplex'
    AUTO_NEGOTIATION = 'Auto Negotiation'
    BANDWIDTH = 'Bandwidth'
    ADJACENT = 'Adjacent'
    IPV4_ADDRESS = 'IPv4 Address'
    IPV6_ADDRESS = 'IPv6 Address'

    def __init__(self, relative_path, **kwargs):
        self._DEFAULT_VALUES[self.PROTOCOL_TYPE] = 'Transparent'
        self._DEFAULT_VALUES[self.L2_PROTOCOL_TYPE] = 'ethernet'
        self._DEFAULT_VALUES[self.MTU] = 0
        self._DEFAULT_VALUES[self.BANDWIDTH] = 0
        super(PortAttributes, self).__init__(relative_path, **kwargs)


class PortChannelAttributes(AttributeContainer):
    PROTOCOL_TYPE = 'Protocol Type'
    PORT_DESCRIPTION = 'Port Description'
    ASSOCIATED_PORTS = 'Associated Ports'
    IPV4_ADDRESS = 'IPv4 Address'
    IPV6_ADDRESS = 'IPv6 Address'

    def __init__(self, relative_path, **kwargs):
        self._DEFAULT_VALUES[self.PROTOCOL_TYPE] = 'Transparent'
        super(PortChannelAttributes, self).__init__(relative_path, **kwargs)


class PowerPortAttributes(AttributeContainer):
    SERIAL_NUMBER = 'Serial Number'
    MODEL = 'Model'
    VERSION = 'Version'
    PORT_DESCRIPTION = 'Port Description'
