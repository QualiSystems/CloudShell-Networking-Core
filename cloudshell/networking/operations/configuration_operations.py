import traceback

from abc import abstractmethod
from cloudshell.core.action_result import ActionResult
from cloudshell.core.driver_response import DriverResponse
from cloudshell.core.driver_response_root import DriverResponseRoot
from cloudshell.networking.core.connectivity_request_helper import ConnectivityRequestDeserializer
from cloudshell.networking.interfaces.orchestration.save_response import OrchestrationSaveResponse
from cloudshell.networking.operations.interfaces.configuration_operations_interface import \
    ConfigurationOperationsInterface

import jsonpickle


class ConfigurationOperations(ConfigurationOperationsInterface):
    REQUEST_REQUIRED_ATTRIBUTE_LIST = ['type', 'actionId', ('connectionParams', 'mode'), ('actionTarget', 'fullAddress')]

    def __init__(self):
        pass

    @property
    @abstractmethod
    def logger(self):
        pass

    def orchestration_save(self, context, mode="shallow", custom_params=None):
        """Handle apply connectivity changes request json, trigger add or remove vlan methods,
        get responce from them and create json response

        :param request: json with all required action to configure or remove vlans from certain port
        :return Serialized DriverResponseRoot to json
        :rtype json
        """

        if custom_params is None or custom_params == '':
            raise Exception('ConfigurationOperations', 'request is None or empty')

        params = ConnectivityRequestDeserializer(jsonpickle.decode(custom_params))

        if not params or not hasattr(params, 'driverRequest'):
            raise Exception('ConfigurationOperations', 'Deserialized request is None or empty')

        save_response = OrchestrationSaveResponse()

        self.logger.info('Action: ', params.__dict__)
        self._validate_request_action(params)
        result = self.save_configuration(configuration_type=params.configuration_type, folder_path=params.folder_path,
                                vrf_management_name=params.vrf_management_name)

        save_response.saved_artifact_info.resource_name =self.resource_name
        save_response.saved_artifact.resource_id = '5F2EAA6C-E3FD-4DF0-8E2D-F05C81D61631'
        # TODO where should we retrieve resource id?
        save_response.saved_artifact.identifier = result

        return self.set_command_result(save_response).replace('[true]', 'true')

    def orchestration_restore(self, context, saved_artifact_info, custom_params=None):
        """Handle apply connectivity changes request json, trigger add or remove vlan methods,
        get responce from them and create json response

        :param request: json with all required action to configure or remove vlans from certain port
        :return Serialized DriverResponseRoot to json
        :rtype json
        """

        if saved_artifact_info is None or saved_artifact_info == '':
            raise Exception('ConfigurationOperations', 'saved_artifact_info is None or empty')

        if custom_params is None or custom_params == '':
            raise Exception('ConfigurationOperations', 'custom_params is None or empty')

        # saved_artifact = ConnectivityRequestDeserializer(jsonpickle.decode(saved_artifact_info))
        # params = ConnectivityRequestDeserializer(jsonpickle.decode(custom_params))
        # driver_response = OrchestrationSaveResponse()
        #
        # self.logger.info('Restore: ', params.__dict__)
        # self._validate_request_action(params)
        # return self.set_command_result(driver_response_root).replace('[true]', 'true')

    def _validate_request_action(self, action):
        """Validate action from the request json, according to APPLY_CONNECTIVITY_CHANGES_ACTION_REQUIRED_ATTRIBUTE_LIST

        """
        is_fail = False
        fail_attribute = ''
        for class_attribute in self.REQUEST_REQUIRED_ATTRIBUTE_LIST:
            if type(class_attribute) is tuple:
                if not hasattr(action, class_attribute[0]):
                    is_fail = True
                    fail_attribute = class_attribute[0]
                if not hasattr(getattr(action, class_attribute[0]), class_attribute[1]):
                    is_fail = True
                    fail_attribute = class_attribute[1]
            else:
                if not hasattr(action, class_attribute):
                    is_fail = True
                    fail_attribute = class_attribute

        if is_fail:
            raise Exception('ConnectivityOperations',
                            'Mandatory field {0} is missing in ApplyConnectivityChanges request json'.format(
                                fail_attribute))

    def set_command_result(self, result, unpicklable=False):
        """Serializes output as JSON and writes it to console output wrapped with special prefix and suffix

        :param result: Result to return
        :param unpicklable: If True adds JSON can be deserialized as real object.
                            When False will be deserialized as dictionary
        """

        json = jsonpickle.encode(result, unpicklable=unpicklable)
        result_for_output = str(json)
        return result_for_output

    @abstractmethod
    def add_vlan(self, vlan_range, port_list, port_mode, qnq, ctag):
        pass

    @abstractmethod
    def remove_vlan(self, vlan_range, port_list, port_mode):
        pass
