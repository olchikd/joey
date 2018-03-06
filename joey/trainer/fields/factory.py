from fields import BaseField
from ..utils import fill_type_map

TYPE_MAP = fill_type_map(BaseField)


class FieldFactory(object):
    @classmethod
    def factory(cls, data):
        name = data.get('name')
        feature_type = data.get('type', 'string')
        is_required = data.get('is_required', True)
        parameters = data.get('parameters', [])
        default = data.get('default', None)
        return TYPE_MAP[feature_type](name, is_required, parameters, default)
