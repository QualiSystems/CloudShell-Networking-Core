class ActionTarget:

    def __init__(self, full_name='', full_address=''):
        """
        Describes a connectivity action target
        :param str full_name: full resource name
        :param str full_address: full resource address
        """
        self.fullName = full_name
        """:type : str"""
        self.fullAddress = full_address
        """:type : str"""
        self.type = "actionTarget"
        """:type : str"""

    @classmethod
    def from_dict(cls, dictionary):
        return ActionTarget(full_name=dictionary['fullName'], full_address=dictionary['fullAddress'])