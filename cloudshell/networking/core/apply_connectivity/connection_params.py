
from cloudshell.networking.core.apply_connectivity.atribute_name_value import AttributeNameValue


class ConnectionParams(object):
    def __init__(self, type='', vlan_id='', mode='', vlan_service_attributes=[]):
        """
        :param str type:
        :param str vlan_id:
        :param str mode:
        :param list[AttributeNameValue] vlan_service_attributes:
        """
        self.type = type
        self.vlanId = vlan_id
        self.mode = mode
        self.vlanServiceAttributes= vlan_service_attributes
        self.type='setVlanParameter'


    @classmethod
    def from_dict(cls, dictionary):
        con_params = ConnectionParams()
        con_params.type = dictionary['type']
        con_params.vlanServiceAttributes = [AttributeNameValue.from_dict(attr) for attr
                                            in dictionary['vlanServiceAttributes']]
        con_params.mode = dictionary['mode']
        return con_params
