from cloudshell.shell.core.driver_context import AutoLoadAttribute


class AttributeContainer(list):
    _DEFAULT_VALUE = ''
    _DEFAULT_VALUES = {}

    def __init__(self, relative_path=None, **attributes_dict):
        self._default_values = {}
        self.handle_attributes_dict(relative_path, attributes_dict)

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
