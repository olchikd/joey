from ..exceptions import ProcessingFieldException


class BaseField(object):
    type_name = None

    def __init__(self, name, is_required, parameters, default):
        self.name = name
        self.is_required = is_required
        self.parameters = parameters
        self.default = default

    def process(self, value):
        value = self.apply_type(value)
        if value is None:
            if not self.default is None:
                value = self.default
            else:
                raise ProcessingFieldException("missing {0}".format(self.name))
        return value

    def apply_type(self, value):
        raise NotImplemented()


class BaseSimpleField(BaseField):
    simple_type = str

    def apply_type(self, value):
        return self.simple_type(value)


class StringField(BaseSimpleField):
    type_name = "string"
    simple_type = str


class StringField(BaseSimpleField):
    type_name = "integer"
    simple_type = int


class StringField(BaseSimpleField):
    type_name = "float"
    simple_type = float
