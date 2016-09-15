import uuid

import jsonpickle
from cloudshell.core.driver_request import DriverRequest
from mock import Mock, MagicMock

from cloudshell.networking.apply_connectivity.action_request import ActionRequest
from cloudshell.networking.apply_connectivity.action_target import ActionTarget
from cloudshell.networking.apply_connectivity.connection_params import ConnectionParams
from cloudshell.networking.apply_connectivity.vlanServiceAttribute import VlanServiceAttribute
from cloudshell.networking.standard.standard_connectivity import StandardApplyConnectivityImplementation, \
    ConnectivitySuccessResponse, ConnectivityActionRequest

__author__ = 'wise__000'

import unittest


class DriverRequestSimulation:
    def __init__(self, request):
        self.driverRequest = request


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = Mock()
        self.apply_connectivity = StandardApplyConnectivityImplementation()

    def test_it_delegates_all_add_vlan_calls_to_supplied_callback(self):
        unique_message = 'Unique Result'

        add_vlan_function = MagicMock(side_effect=lambda action: ConnectivitySuccessResponse(action, unique_message))

        # Arrange
        set_vlan_action = self._stub_set_vlan_action(full_address='192.1.3.4/1', full_name='res1/port1', vlan_id='200')

        server_request = DriverRequest()
        server_request.actions = [set_vlan_action]
        request_json = jsonpickle.encode(DriverRequestSimulation(server_request), unpicklable=False)

        # Act
        result = self.apply_connectivity.standard_apply_connectivity_changes(request=request_json,
                                                                             logger=self.logger,
                                                                             add_vlan_action=add_vlan_function,
                                                                             remove_vlan_action=[])

        # Assert
        add_vlan_function.assert_called_once()
        result_object = jsonpickle.decode(result)
        # We validate that the action was delegated by looking for th eunique value we returned
        self.assertEqual(result_object['driverResponse']['actionResults'][0]['infoMessage'], unique_message)

    def test_it_delegates_all_remove_vlan_calls_to_supplied_callback(self):
        unique_message = 'Unique Result'
        remove_vlan_function = MagicMock(side_effect=lambda action: ConnectivitySuccessResponse(action, unique_message))

        # Arrange
        set_vlan_action = self._stub_remove_vlan_action(full_address='192.1.3.4/1', full_name='res1/port1',
                                                        vlan_id='200')

        server_request = DriverRequest()
        server_request.actions = [set_vlan_action]
        request_json = jsonpickle.encode(DriverRequestSimulation(server_request), unpicklable=False)

        # Act
        result = self.apply_connectivity.standard_apply_connectivity_changes(request=request_json,
                                                                             logger=self.logger,
                                                                             add_vlan_action=[],
                                                                             remove_vlan_action=remove_vlan_function)
        # Assert
        remove_vlan_function.assert_called_once()
        result_object = jsonpickle.decode(result)
        # We validate that the action was delegated by looking for th eunique value we returned
        self.assertEqual(result_object['driverResponse']['actionResults'][0]['infoMessage'], unique_message)

    def test_it_merges_the_result_of_all_callbacks_to_one_result_object(self):
        unique_message = 'Unique Result'

        add_vlan_function = MagicMock(side_effect=lambda action: ConnectivitySuccessResponse(action, unique_message))

        # Arrange
        set_vlan_action_1 = self._stub_set_vlan_action(full_address='192.1.3.4/1', full_name='res1/port1',
                                                       vlan_id='200')
        set_vlan_action_2 = self._stub_set_vlan_action(full_address='192.1.3.4/2', full_name='res1/port2',
                                                       vlan_id='201')
        set_vlan_action_3 = self._stub_set_vlan_action(full_address='192.1.3.4/3', full_name='res1/port3',
                                                       vlan_id='202')
        set_vlan_action_4 = self._stub_set_vlan_action(full_address='192.1.3.4/4', full_name='res1/port4',
                                                       vlan_id='203')

        server_request = DriverRequest()
        server_request.actions = [
            set_vlan_action_1,
            set_vlan_action_2,
            set_vlan_action_3,
            set_vlan_action_4
        ]
        request_json = jsonpickle.encode(DriverRequestSimulation(server_request), unpicklable=False)

        # Act
        result = self.apply_connectivity.standard_apply_connectivity_changes(request=request_json,
                                                                             logger=self.logger,
                                                                             add_vlan_action=add_vlan_function,
                                                                             remove_vlan_action=[])

        # Assert
        add_vlan_function.assert_called()
        result_object = jsonpickle.decode(result)
        # We validate that the action was delegated by looking for th eunique value we returned
        returned_results = result_object['driverResponse']['actionResults']
        self.assertEqual(len(returned_results), 4)
        for result in returned_results:
            self.assertEqual(result['infoMessage'], unique_message)


    @staticmethod
    def _stub_set_vlan_action(full_address='192.1.3.4/1', full_name='rest1/port1', vlan_id='200'):
        action = ActionRequest()
        action.actionId = str(uuid.uuid4())
        action.type = ConnectivityActionRequest.SET_VLAN
        action.actionTarget = ActionTarget(full_address=full_address,
                                           full_name=('%s' % full_name))
        action.connectionId = str(uuid.uuid4())
        action.connectionParams = ConnectionParams(mode='Access', vlanId=vlan_id,
                                                   vlan_service_attributes=[
                                                       VlanServiceAttribute(attribute_name='QNQ',
                                                                            attribute_value='false')
                                                   ])
        return action

    @staticmethod
    def _stub_remove_vlan_action(full_address='192.1.3.4/1', full_name='rest1/port1', vlan_id='200'):
        action = ActionRequest()
        action.actionId = str(uuid.uuid4())
        action.type = ConnectivityActionRequest.REMOVE_VLAN
        action.actionTarget = ActionTarget(full_address=full_address,
                                           full_name=('%s' % full_name))
        action.connectionId = str(uuid.uuid4())
        action.connectionParams = ConnectionParams(mode='Access', vlanId=vlan_id,
                                                   vlan_service_attributes=[
                                                       VlanServiceAttribute(attribute_name='QNQ',
                                                                            attribute_value='false')
                                                   ])
        return action


if __name__ == '__main__':
    unittest.main()
