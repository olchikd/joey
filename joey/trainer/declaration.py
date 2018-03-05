import json
import importlib
from collections import OrderedDict

from exceptions import ModelJsonException, ModelDeclarationException
from fields.factory import FieldFactory


class Declaration(object):
    REQUIRED_KEYS = ('output_field', 'fieldset', 'algorithm')

    def __init__(self, data):
            data = json.loads(data)
        except Exception as e:
            raise ModelJsonException(e)

        _validate(data)

        # Algo part of the configuration
        algorithm_config = data.get('algorithm', None)
        if algorithm_config is None:
            raise ModelDeclarationException('ML algo declaration not found')

        self.algo_class = classifier_config.get('class')
        self.algo_type = classifier_config.get('type')
        self.parameters = parameters

        module, name = self.algo_class.rsplit(".", 1)
        module = importlib.import_module(module)
        self.algo_cls = getattr(module, name)

        self.group = data.get("group")

        # dataset fields declaration
        self.output_field = data.get("output_field")
        self.fieldset = OrderedDict()
        self.required_fields = []
        for field_data in data['fieldset']:
            self._validate_field(field)

            field = FieldFactory.factory(field_data)
            if field.is_required:
                self.required_fields.append(field.name)

            self.fieldset[field.name] = field

    def _validate(self, data):
        for key in REQUIRED_KEYS:
            if not key in data:
                raise ModelDeclarationException(
                    "missing element {0}".format(key))

    def _validate_field(self, field):
        if not ('name' in feature and 'type' in field):
            raise ModelDeclarationException('missing in {0} decl'.format(field))
