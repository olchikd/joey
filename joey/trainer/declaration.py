import json
import importlib
from collections import OrderedDict

from exceptions import ModelJsonException, ModelDeclarationException
from fields.factory import FieldFactory


class Declaration(object):
    REQUIRED_KEYS = ('output_field', 'fieldset', 'algorithm')

    def __init__(self, data):
        try:
            data = json.loads(data)
        except Exception as e:
            raise ModelJsonException(e)

        self._validate(data)

        # Algo part of the configuration
        algorithm_config = data.get('algorithm', None)
        if algorithm_config is None:
            raise ModelDeclarationException('ML algo declaration not found')

        self.algo_class = algorithm_config.get('class')
        self.algo_type = algorithm_config.get('type', 'classification')
        self.parameters = algorithm_config.get('parameters')

        module, name = self.algo_class.rsplit(".", 1)
        module = importlib.import_module(module)
        self.algo_cls = getattr(module, name)

        self.group = data.get("group")

        # dataset fields declaration
        self.output_field = data.get("output_field")
        self.fieldset = OrderedDict()
        self.required_fields = []
        for field_data in data['fieldset']:
            self._validate_field(field_data)

            field = FieldFactory.factory(field_data)
            if field.is_required:
                self.required_fields.append(field.name)

            self.fieldset[field.name] = field

    @property
    def y_field(self):
        return self.fieldset[self.output_field]

    def _validate(self, data):
        for key in Declaration.REQUIRED_KEYS:
            if not key in data:
                raise ModelDeclarationException(
                    "missing element {0}".format(key))

    def _validate_field(self, field):
        if not ('name' in field and 'type' in field):
            raise ModelDeclarationException('missing in {0} decl'.format(field))
