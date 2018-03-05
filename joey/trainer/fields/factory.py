from fields import BaseField
from utils import all_subclasses


TYPE_MAP = {}
# TODO: Lookup to folder in the config
for field in all_subclasses(BaseField):
    if not field.type_name is None:
        TYPE_MAP[field.type_name] = cls


class FieldFactory(object):
    @classmethod
    def factory(cls, data):
        name = data.get('name')
        feature_type = data.get('type', 'string')
        is_required = data.get('is_required', True)
        parameters = data.get('parameters', [])
        default = data.get('default', None)
        return TYPE_MAP[feature_type](name, required, parameters, default)
