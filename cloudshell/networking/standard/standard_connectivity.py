import traceback
import jsonpickle
from cloudshell.core.action_result import ActionResult
from cloudshell.core.driver_response import DriverResponse
from cloudshell.core.driver_response_root import DriverResponseRoot
from cloudshell.networking.core.json_request_helper import JsonRequestDeserializer

class ConnectivityRequest:
    SET_VLAN = 'setVlan'
    REMOVE_VLAN = 'removeVlan'


class StandardApplyConnectivityImplementation(object):
    def standard_apply_connectivity_changes(self, request, logger,
                                            add_vlan_action,
                                            remove_vlan_action):
        """Handle apply connectivity changes request json, trigger add or remove vlan methods,
        get responce from them and create json response

        :param request: json with all required action to configure or remove vlans from certain port
        :return Serialized DriverResponseRoot to json
        :rtype json
        """

        if request is None or request == '':
            raise Exception('ConnectivityOperations', 'request is None or empty')

        holder = JsonRequestDeserializer(jsonpickle.decode(request))

        if not holder or not hasattr(holder, 'driverRequest'):
            raise Exception('ConnectivityOperations', 'Deserialized request is None or empty')

        driver_response = DriverResponse()
        results = []
        driver_response_root = DriverResponseRoot()

        for action in holder.driverRequest.actions:
            logger.info('Action: ', action.__dict__)
            if action.type == ConnectivityRequest.SET_VLAN:
                action_result = add_vlan_action(action)

            elif action.type == ConnectivityRequest.REMOVE_VLAN:
                action_result = remove_vlan_action(action)

            else:
                continue
            results.append(action_result)

        driver_response.actionResults = results
        driver_response_root.driverResponse = driver_response
        return self.set_command_result(driver_response_root).replace('[true]', 'true')

    def set_command_result(self, result, unpicklable=False):
        """Serializes output as JSON and writes it to console output wrapped with special prefix and suffix

        :param result: Result to return
        :param unpicklable: If True adds JSON can be deserialized as real object.
                            When False will be deserialized as dictionary
        """

        json = jsonpickle.encode(result, unpicklable=unpicklable)
        result_for_output = str(json)
        return result_for_output


class ConnectivitySuccessResponse(ActionResult):
    def __init__(self, action, result_string):
        ActionResult.__init__(self)
        self.type = action.type
        self.actionId = action.actionId
        self.errorMessage = None
        self.updatedInterface = action.actionTarget.fullName
        self.infoMessage = result_string


class ConnectivityErrorResponse(ActionResult):
    def __init__(self, action, error_string):
        ActionResult.__init__(self)
        self.type = action.type
        self.actionId = action.actionId
        self.infoMessage = None
        self.updatedInterface = action.actionTarget.fullName
        self.errorMessage = error_string
        self.success = False
