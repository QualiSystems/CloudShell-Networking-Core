class AttributeNameValue(object):
    def __init__(self, attribute_name='', attribute_value='', type=''):
        """
        Describes an attribute name value
        :param str attribute_name: Attribute name
        :param str attribute_value: Attribute value
        :param str type: Object type
        """

        self.type = type
        """:type : str"""
        self.attributeName = attribute_name
        """:type : str"""
        self.attributeValue = attribute_value
        """:type : str"""

    @classmethod
    def from_dict(cls, dictionary):
        att = AttributeNameValue()
        att.type = dictionary['type']
        att.attributeName = dictionary['attributeName']
        att.attributeValue = dictionary['attributeValue']
        return att
