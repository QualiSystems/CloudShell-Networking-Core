from cloudshell.shell.core.driver_context import AutoLoadResource
from cloudshell.networking.autoload.networking_autoload_resource_attributes import ChassisAttributes, \
    PowerPortAttributes, PortAttributes, ModuleAttributes, SubModuleAttributes, PortChannelAttributes, \
    AttributeContainer, RootAttributes


class GenericResource(AutoLoadResource):
    ATTRIBUTE_CONTAINER = AttributeContainer
    MODEL = 'Generic Resource'
    NAME_TEMPLATE = 'Resource{0}'
    RELATIVE_PATH_TEMPLATE = '{0}/{1}'

    def __init__(self, element_id, name=None, model=None, relative_path=None, unique_id=None,
                 **attributes_dict):

        self.element_id = element_id
        if name is not None and name != '':
            self.name = name
        elif self.NAME_TEMPLATE is not None:
            self.name = self.NAME_TEMPLATE.format(self.element_id)
        else:
            self.name = None

        if model is not None and model != '':
            self.model = model
        else:
            self.model = self.MODEL

        if relative_path is not None and relative_path != '':
            self.relative_address = relative_path
        else:
            self.relative_address = None

        if unique_id is not None and unique_id != '':
            self.unique_identifier = unique_id

        if attributes_dict is not None and len(attributes_dict) > 0:
            self.attributes = self.ATTRIBUTE_CONTAINER(**attributes_dict)
        else:
            self.attributes = []

    def build_attributes(self, attributes_dict):
        if self.attributes is None or len(self.attributes) == 0:
            self.attributes = self.ATTRIBUTE_CONTAINER(self.relative_address, **attributes_dict)

    def build_relative_path(self, parent_path):
        if self.RELATIVE_PATH_TEMPLATE is None:
            self.relative_address = ''
        elif parent_path is not None and parent_path != '':
            self.relative_address = self.RELATIVE_PATH_TEMPLATE.format(parent_path, self.element_id)
        else:
            self.relative_address = self.RELATIVE_PATH_TEMPLATE.format(self.element_id)

        self._set_relative_path_to_attributes()

    def _build_relative_path_for_child_resources(self, parent_path, *child_resources):
        for child_list in child_resources:
            self._build_relative_path_for_resource_list(parent_path, child_list)

    def _build_relative_path_for_resource_list(self, parent_path, child_resources):
        if child_resources is not None and len(child_resources) > 0:
            for resource in child_resources:
                resource.build_relative_path(parent_path)

    def _set_relative_path_to_attributes(self):
        for attribute in self.attributes:
            attribute.relative_address = self.relative_address

    def get_attributes(self):
        return self.attributes

    def _get_attributes_for_child_resources(self, *child_resources):
        attributes = []
        if len(child_resources) > 0:
            for res_list in child_resources:
                attributes += self._get_attributes_for_resource_list(res_list)
        return attributes

    def _get_attributes_for_resource_list(self, resource_list):
        attributes = []
        for resource in resource_list:
            attributes += resource.get_attributes()
        return attributes

    def get_resources(self):
        return [self]

    def _get_resources_for_child_resources(self, *child_resources):
        resources = []
        for resource_list in child_resources:
            resources += self._get_resources_for_resource_list(resource_list)
        return resources

    def _get_resources_for_resource_list(self, resource_list):
        resources = []
        for resource in resource_list:
            resources += resource.get_resources()
        return resources


class RootElement(GenericResource):
    ATTRIBUTE_CONTAINER = RootAttributes
    MODEL = None
    NAME_TEMPLATE = None
    RELATIVE_PATH_TEMPLATE = None

    def __init__(self, element_id=None, **attributes_dict):
        GenericResource.__init__(self, element_id, **attributes_dict)
        self.chassis = []
        self.port_channels = []

    def build_relative_path(self, parent_path=None):
        GenericResource.build_relative_path(self, parent_path)
        self._build_relative_path_for_child_resources(self.relative_address, self.chassis, self.port_channels)

    def get_resources(self):
        return self._get_resources_for_child_resources(self.chassis, self.port_channels)

    def get_attributes(self):
        return GenericResource.get_attributes(self) + self._get_attributes_for_child_resources(self.chassis,
                                                                                               self.port_channels)


class Chassis(GenericResource):
    ATTRIBUTE_CONTAINER = ChassisAttributes
    MODEL = 'Generic Chassis'
    NAME_TEMPLATE = 'Chassis{0}'
    RELATIVE_PATH_TEMPLATE = '{0}'

    def __init__(self, element_id, *args, **kwargs):
        GenericResource.__init__(self, element_id)
        self.modules = []
        self.ports = []
        self.power_ports = []

    def build_relative_path(self, parent_path):
        GenericResource.build_relative_path(self, parent_path)
        self._build_relative_path_for_child_resources(self.relative_address, self.modules, self.ports, self.power_ports)

    def get_attributes(self, *args):
        return GenericResource.get_attributes(self) + self._get_attributes_for_child_resources(self.modules, self.ports,
                                                                                               self.power_ports)

    def get_resources(self):
        return GenericResource.get_resources(self) + self._get_resources_for_child_resources(self.modules, self.ports,
                                                                                             self.power_ports)


class PowerPort(GenericResource):
    ATTRIBUTE_CONTAINER = PowerPortAttributes
    MODEL = 'Generic Power Port'
    NAME_TEMPLATE = 'PP{0}'
    RELATIVE_PATH_TEMPLATE = '{0}/PP{1}'

    def __init__(self, element_id, *args, **kwargs):
        GenericResource.__init__(self, element_id)


class Port(GenericResource):
    ATTRIBUTE_CONTAINER = PortAttributes
    MODEL = 'Generic Port'
    NAME_TEMPLATE = '{0}'
    RELATIVE_PATH_TEMPLATE = '{0}/{1}'

    def __init__(self, element_id, name, *args, **kwargs):
        GenericResource.__init__(self, element_id, name=name)


class PortChannel(GenericResource):
    ATTRIBUTE_CONTAINER = PortChannelAttributes
    MODEL = 'Generic Port Channel'
    NAME_TEMPLATE = '{0}'
    RELATIVE_PATH_TEMPLATE = 'PC{0}'

    def __init__(self, element_id, name, *args, **kwargs):
        GenericResource.__init__(self, element_id, name=name)


class Module(GenericResource):
    ATTRIBUTE_CONTAINER = ModuleAttributes
    MODEL = 'Generic Module'
    NAME_TEMPLATE = 'Module{0}'
    RELATIVE_PATH_TEMPLATE = '{0}/{1}'

    def __init__(self, element_id, *args, **kwargs):
        GenericResource.__init__(self, element_id)
        self.sub_modules = []
        self.ports = []

    def build_relative_path(self, parent_path):
        GenericResource.build_relative_path(self, parent_path)
        self._build_relative_path_for_child_resources(self.relative_address, self.sub_modules, self.ports)

    def get_resources(self):
        return GenericResource.get_resources(self) + self._get_resources_for_child_resources(self.sub_modules,
                                                                                             self.ports)

    def get_attributes(self):
        return GenericResource.get_attributes(self) + self._get_attributes_for_child_resources(self.sub_modules,
                                                                                               self.ports)


class SubModule(GenericResource):
    ATTRIBUTE_CONTAINER = SubModuleAttributes
    MODEL = 'Generic Sub Module'
    NAME_TEMPLATE = 'SubModule{0}'
    RELATIVE_PATH_TEMPLATE = '{0}/{1}'

    def __init__(self, element_id, *args, **kwargs):
        GenericResource.__init__(self, element_id)
        self.ports = []

    def build_relative_path(self, parent_path):
        GenericResource.build_relative_path(self, parent_path)
        self._build_relative_path_for_child_resources(self.relative_address, self.ports)

    def get_resources(self):
        return GenericResource.get_resources(self) + self._get_resources_for_child_resources(self.ports)

    def get_attributes(self):
        return GenericResource.get_attributes(self) + self._get_attributes_for_child_resources(self.ports)
