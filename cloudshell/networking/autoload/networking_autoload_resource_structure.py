from cloudshell.shell.core.driver_context import AutoLoadResource
from cloudshell.networking.autoload.networking_autoload_resource_attributes import ChassisAttributes, \
    PowerPortAttributes, PortAttributes, ModuleAttributes, PortChannelAttributes, GenericResourceAttributes


class GenericResource(AutoLoadResource):
    ATTRIBUTES_CLASS = GenericResourceAttributes
    MODEL = 'Generic Resource'
    NAME_TEMPLATE = 'Resource{0}'
    RELATIVE_PATH_TEMPLATE = '{0}/{1}'

    def __init__(self, element_id, name=None, model=None, relative_path=None, unique_id=None,
                 **attributes_dict):

        self.element_id = element_id
        if name is not None and name != '':
            self.name = name
        else:
            self.name = self.NAME_TEMPLATE.format(self.element_id)
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
            self.attributes = self.ATTRIBUTES_CLASS(**attributes_dict)
        else:
            self.attributes = []

    def build_attributes(self, attributes_dict):
        if self.attributes is None or len(self.attributes) == 0:
            self.attributes = self.ATTRIBUTES_CLASS(**attributes_dict)

    def build_relative_path(self, parent_path):
        if self.relative_address is None or self.relative_address == '':
            if parent_path is not None:
                self.relative_address = self.RELATIVE_PATH_TEMPLATE.format(parent_path, self.element_id)
            else:
                self.relative_address = self.RELATIVE_PATH_TEMPLATE.format(self.element_id)
        self._set_relative_path_to_attributes()

    def _build_relative_path_for_childs(self, child_resources, parent_path):
        if child_resources is not None and len(child_resources) > 0:
            for resource in child_resources:
                resource.build_relative_path(parent_path)

    def _set_relative_path_to_attributes(self):
        for attribute in self.attributes:
            attribute.relative_address = self.relative_address


class Chassis(GenericResource):
    ATTRIBUTES_CLASS = ChassisAttributes
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
        self._build_relative_path_for_childs(self.modules, self.relative_address)
        self._build_relative_path_for_childs(self.ports, self.relative_address)
        self._build_relative_path_for_childs(self.power_ports, self.relative_address)


class PowerPort(GenericResource):
    ATTRIBUTES_CLASS = PowerPortAttributes
    MODEL = 'Generic Power Port'
    NAME_TEMPLATE = 'PP{0}'
    RELATIVE_PATH_TEMPLATE = '{0}/PP{1}'

    def __init__(self, element_id, *args, **kwargs):
        GenericResource.__init__(self, element_id)


class Port(GenericResource):
    ATTRIBUTES_CLASS = PortAttributes
    MODEL = 'Generic Port'
    NAME_TEMPLATE = '{0}'
    RELATIVE_PATH_TEMPLATE = '{0}/{1}'

    def __init__(self, element_id, name, *args, **kwargs):
        GenericResource.__init__(self, element_id, name=name)


class PortChannel(GenericResource):
    ATTRIBUTES_CLASS = PortChannelAttributes
    MODEL = 'Generic Port Channel'
    NAME_TEMPLATE = '{0}'
    RELATIVE_PATH_TEMPLATE = 'PC{0}'

    def __init__(self, element_id, name, *args, **kwargs):
        GenericResource.__init__(self, element_id, name=name)


class Module(GenericResource):
    ATTRIBUTES_CLASS = ModuleAttributes
    MODEL = 'Generic Module'
    NAME_TEMPLATE = 'Module{0}'
    RELATIVE_PATH_TEMPLATE = '{0}/{1}'

    def __init__(self, element_id, *args, **kwargs):
        GenericResource.__init__(self, element_id)
        self.sub_modules = []
        self.ports = []

    def build_relative_path(self, parent_path):
        GenericResource.build_relative_path(self, parent_path)
        self._build_relative_path_for_childs(self.sub_modules, self.relative_address)
        self._build_relative_path_for_childs(self.ports, self.relative_address)


class SubModule(GenericResource):
    ATTRIBUTES_CLASS = ModuleAttributes
    MODEL = 'Generic Sub Module'
    NAME_TEMPLATE = 'SubModule{0}'
    RELATIVE_PATH_TEMPLATE = '{0}/{1}'

    def __init__(self, element_id, *args, **kwargs):
        GenericResource.__init__(self, element_id)
        self.ports = []

    def build_relative_path(self, parent_path):
        GenericResource.build_relative_path(self, parent_path)
        self._build_relative_path_for_childs(self.ports, self.relative_address)
