__author__ = 'CoYe'

from abc import ABCMeta
from abc import abstractmethod

class NetworkingResourceDriverInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def Add_VLAN(self, matrixJSON, ports, VLAN_Ranges, VLAN_Mode, Additional_Info):
        pass

    @abstractmethod
    def Remove_VLAN(self, matrixJSON, ports, VLAN_Ranges, VLAN_Mode, Additional_Info):
        pass

    @abstractmethod
    def SendCustomCommand(self, command):
        pass

    @abstractmethod
    def Save(self, matrixJSON, folder_path, configuration_type):
        pass

    @abstractmethod
    def Restore(self, path, restore_method):
        pass

    @abstractmethod
    def GetInventory(self, matrixJSON):
        pass

    @abstractmethod
    def UpdateFirmware(self, matrixJSON, remote_host, file_path):
        pass

    @abstractmethod
    def Shutdown(self):
        pass
