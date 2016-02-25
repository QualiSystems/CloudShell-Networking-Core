__author__ = 'CoYe'

from abc import ABCMeta
from abc import abstractmethod

class NetworkingResourceDriverInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_vlan(self, matrixJSON, ports, VLAN_Ranges, VLAN_Mode, Additional_Info):
        pass

    @abstractmethod
    def remove_vlan(self, matrixJSON, ports, VLAN_Ranges, VLAN_Mode, Additional_Info):
        pass

    @abstractmethod
    def send_custom_command(self, matrixJSON, command):
        pass

    @abstractmethod
    def send_custom_config_command(self, matrixJSON, command):
        pass

    @abstractmethod
    def save(self, matrixJSON, folder_path, configuration_type):
        pass

    @abstractmethod
    def restore(self, path, restore_method):
        pass

    @abstractmethod
    def get_inventory(self, matrixJSON):
        pass

    @abstractmethod
    def load_firmware(self, matrixJSON, remote_host, file_path):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
