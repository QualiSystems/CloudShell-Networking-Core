import os
import platform
from abc import abstractmethod
import re
from cloudshell.networking.operations.interfaces.state_operations_interface import StateOperationsInterface


class StateOperations(StateOperationsInterface):
    def __init__(self):
        self.max_allowed_packet_loss = 20
        pass

    @property
    @abstractmethod
    def logger(self):
        pass

    @property
    @abstractmethod
    def resource_name(self):
        pass

    @property
    @abstractmethod
    def cli(self):
        pass

    @property
    @abstractmethod
    def api(self):
        pass

    def health_check(self):
        """Handle apply connectivity changes request json, trigger add or remove vlan methods,
        get responce from them and create json response

        :return Serialized DriverResponseRoot to json
        :rtype json
        """

        result = ''
        success = False
        api_response = 'Online'
        try:
           self.cli.send_command('')
           success = True
        except Exception:
           pass

        result = 'Health check on resource {}'.format(self.resource_name)

        if success:
            result += ' passed;'
        else:
            api_response = 'Error'
            result += ' failed;'

        self.api.SetResourceLiveStatus(self.resource_name, api_response, result)
        return result

    def _get_resource_attribute(self, attribute_name):
        """Get resource attribute by provided attribute_name

        :param resource_full_path: resource name or full name
        :param attribute_name: name of the attribute
        :return: attribute value
        :rtype: string
        """

        try:
            result = self.api.GetAttributeValue(self.resource_name, attribute_name).Value
        except Exception as e:
            raise Exception(e.message)
        return result

    @abstractmethod
    def shutdown(self):
        pass
