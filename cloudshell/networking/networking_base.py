__author__ = 'CoYe'

from cloudshell.shell.core.driver_builder_wrapper import BaseResourceDriver, DriverFunction

class NetworkingBase(BaseResourceDriver):

    def Add_VLAN(self, matrixJSON, ports, VLAN_Ranges, VLAN_Mode, Additional_Info):
        pass

    def Remove_VLAN(self, matrixJSON, ports, VLAN_Ranges, VLAN_Mode, Additional_Info):
        pass

    def SendCustomCommand(self):
        pass

    def Save(self):
        pass

    def Restore(self):
        pass

    def GetInventory(self):
        pass

    def UpdateFirmware(self):
        pass
