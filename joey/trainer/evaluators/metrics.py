import sklearn


class BaseMetric(object):
    type_name = None
    type_names = []
    NAME = "noname"

    def calc(self):
        return 1


class Accuracy(BaseMetric):
    NAME = 'accuracy'
    type_names = ('classification', 'regression')

    def calc(self, original, preds):
        return sklearn.metrics.accuracy_score(original, preds)
