from metrics import BaseMetric
from ..utils import fill_type_list_map


TYPE_MAP = fill_type_list_map(BaseMetric)


class MetricsFactory(object):
    @classmethod
    def factory(cls, model_type):
        """
        Returns list of metrics classes according to
        model type: classification, regression,
        clustering, etc.
        """
        return TYPE_MAP[model_type]
