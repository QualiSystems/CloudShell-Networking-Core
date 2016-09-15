from cloudshell.networking.core.apply_connectivity.action_target import ActionTarget
from cloudshell.networking.core.apply_connectivity.atribute_name_value import AttributeNameValue
from cloudshell.networking.core.apply_connectivity.connection_params import ConnectionParams

class ConnectivityActionRequest(object):
    SET_VLAN = 'setVlan'
    REMOVE_VLAN = 'removeVlan'

    def __init__(self, action_id='', type='', action_target=None, connection_id='', connection_params=[], connector_attributes=[],
                 custom_action_attributes=[]):
        """
        Request to perform a connectivity change
        :param str action_id: An identifier for this action, a response with the corresponding ID is requested
        :param str type: The action type setVlan or removeVlan
        :param ActionTarget action_target: The target resource to apply the connectivity change to
        :param str connection_id: The Id of the connection being updated,
        :param ConnectionParams connection_params: Specific params for the requested connection type
        :param list[AttributeNameValue] connector_attributes: Attributes set on the connector
        :param list[AttributeNameValue] custom_action_attributes: Additional attributes for this action
        """

        self.actionId = action_id
        self.type = type
        self.actionTarget = action_target
        self.connectionId = connection_id
        self.connectionParams = connection_params
        self.connectorAttributes = connector_attributes
        self.customActionAttributes = custom_action_attributes

    @classmethod
    def from_dict(cls, json):
        request = ConnectivityActionRequest()
        request.actionId = json['actionId']
        request.type = json['type']
        request.actionTarget = ActionTarget.from_dict(json['actionTarget'])
        request.connectionId = json['connectionId']
        request.connectionParams = ConnectionParams.from_dict(json['connectionParams'])

        if 'connectorAttributes' in json:
            request.connectorAttributes = [AttributeNameValue.from_dict(attr) for attr
                                           in json['connectorAttributes']]
        else:
            request.connectorAttributes = []

        if 'customActionAttributes' in json:
            request.customActionAttributes = [AttributeNameValue.from_dict(attr) for attr
                                              in json['customActionAttributes']]
        else:
            request.customActionAttributes = []

        return request
