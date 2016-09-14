import re
import uuid
from cloudshell.core.action_request import ActionRequest
from cloudshell.core.action_target import ActionTarget
from cloudshell.core.connection_params import ConnectionParams
from cloudshell.core.vlanServiceAttribute import VlanServiceAttribute
from cloudshell.networking.standard.standard_connectivity import StandardApplyConnectivityImplementation, \
    ConnectivitySuccessResponse
from mock import Mock, MagicMock, call
from cloudshell.tests.standard_connectivity_requests import ADD_VLAN_REQUEST, REMOVE_VLAN_REQUEST, \
    MULTIPLE_ADD_VLAN_REQUEST
from connectivity.action_result import ActionResult

__author__ = 'wise__000'

import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = Mock()
        self.apply_connectivity = StandardApplyConnectivityImplementation()

    def test_it_delegates_all_add_vlan_calls_to_supplied_callback(self):
        add_vlan_function = MagicMock(side_effect=lambda action: ConnectivitySuccessResponse(action, 'Success'))

        request = ActionRequest()
        request.actionId = uuid._uuid_generate_random()
        request.actionTarget = ActionTarget(full_address='192.1.3.4/1', full_name='rest1/port1')
        request.connectionId = uuid._uuid_generate_random()
        request.connectionParams = ConnectionParams(mode='Access', vlanId='200',
                                                    vlan_service_attributes=[
                                                        VlanServiceAttribute(attribute_name='QNQ',
                                                                             attribute_value='false')
                                                    ])

        self.apply_connectivity.standard_apply_connectivity_changes(request=ADD_VLAN_REQUEST,
                                                                    logger=self.logger,
                                                                    add_vlan_action=add_vlan_function,
                                                                    remove_vlan_action=[])

        add_vlan_function.assert_called()

    def test_it_delegates_all_remove_vlan_calls_to_supplied_callback(self):
        self.apply_connectivity.standard_apply_connectivity_changes(request=REMOVE_VLAN_REQUEST,
                                                                    logger=self.logger,
                                                                    add_vlan_action=self.add_vlan_function,
                                                                    remove_vlan_action=self.remove_vlan_function)

        self.remove_vlan_function.assert_called()

    def test_it_merges_the_result_of_all_callbacks_to_one_result_object(self):
        result = self.apply_connectivity.standard_apply_connectivity_changes(request=MULTIPLE_ADD_VLAN_REQUEST,
                                                                             logger=self.logger,
                                                                             add_vlan_action=self.add_vlan_function,
                                                                             remove_vlan_action=self.remove_vlan_function)

    def test_it_passes_all_connection_attributes_to_the_supplied_callback(self):
        pass


if __name__ == '__main__':
    unittest.main()
