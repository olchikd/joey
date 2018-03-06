import logging
import numpy
from scipy.sparse import hstack, csc_matrix
from collections import defaultdict
from evaluators.factory import MetricsFactory


class Trainer(object):
    def __init__(self, declaration):
        self.declaration = declaration

    def get_algo(self):
        algo = self.declaration.algo_cls(**self.declaration.parameters)
        return algo

    def train(self):
        raise NotImplemented()

    def evaluate(self):
        raise NotImplemented()

    def predict(self):
        raise NotImplemented()

    def prepare_data(self, iterator, exclude_output=False):
        processed = 0
        ignored = 0
        vectorized_data = defaultdict(list)
        for row in iterator:
            processed += 1
            try:
                for name, field in self.declaration.fieldset.iteritems():
                    if exclude_output and name == self.declaration.output_field:
                        continue
                    value = field.clean(row.get(name))
                    vectorized_data[name].append(value)
            except Exception, e:
                logging.debug('Ignoring: {0}'.format(e))
                ignored += 1

        logging.info('Processed {0} lines, ignored {1} lines'.format(processed, ignored))
        return vectorized_data, processed, ignored

    def predict_proba(self, model, vectorized_data):
        x_matrix, y_vector = self._extract_fields(vectorized_data)
        predict_data = get_matrix_or_vector(x_matrix)
        return model.predict_proba(predict_data)

    def _extract_fields(self, vectorized_data):
        """
        Gets X and y from vectorized data.
        """
        logging.info('Extracting fields.')
        x_matrix = []
        y_vector = None
        for name, field in self.declaration.fieldset.iteritems():
            if name == self.declaration.output_field:
                y_vector = vectorized_data[name]
            else:
                item = self.prepare_column(field, vectorized_data[name])
                if item is not None:
                    # Convert item to csc_matrix, since hstack fails with arrays
                    x_matrix.append(csc_matrix(item))
        return x_matrix, y_vector

    def _to_column(self, x):
        return numpy.transpose(
            csc_matrix([0.0 if item is None else float(item) for item in x]))


class GroupModelsTrainer(Trainer):
    pass


class PlainTrainer(Trainer):
    def train(self, iterator):
        vectorized_data, processed, ignored = self.prepare_data(iterator)
        x_matrix, y_vector = self._extract_fields(vectorized_data)

        logging.info('Training model.')
        try:
            true_data = hstack(x_matrix)
        except ValueError:
            true_data = numpy.hstack(x_matrix)

        algo = self.get_algo()
        algo.fit(true_data, [str(l) for l in y_vector])
        return algo

    def evaluate(self, model, iterator):
        result = {}
        vectorized_data, processed, ignored = self.prepare_data(iterator)
        x_matrix, y_vector = self._extract_fields(vectorized_data)
        predict_data = get_matrix_or_vector(x_matrix)
        probs = model.predict_proba(predict_data)

        # TODO: now only classification
        output_field = self.declaration.y_field
        predicted_str = model.classes_[probs.argmax(axis=1)]
        y_predicted = []
        for y in predicted_str:
            y_predicted.append(output_field.clean(y))

        # print "_______ y _______"
        # for yo, yp in zip(y_vector, y_predicted):
        #     print yo, yp, yo == yp

        result = {'y_vector': y_vector, 'y_predicted': y_predicted}
        metrics = {}
        metrics_classes_list = MetricsFactory.factory(self.declaration.algo_type)
        for metric_class in  metrics_classes_list:
            mhelper = metric_class()
            metrics[mhelper.NAME] = mhelper.calc(y_vector, y_predicted)
        result['metrics'] = metrics
        return result

    def predict(self, model, iterator):
        vectorized_data, processed, ignored = self.prepare_data(
            iterator, exclude_output=True)
        probs = self.predict_proba(model, vectorized_data)
        result = {
            'probs': probs,
        }
        # FIXME:
        if hasattr(model, "classes_"):
            result["classes"] = model.classes_
            result["labels"] = model.classes_[probs.argmax(axis=1)]
        return result

    def prepare_column(self, field, data):
        return self._to_column(data)


def get_matrix_or_vector(x_matrix):
    if(len(x_matrix) == 1):
        return numpy.array(x_matrix[0])
    else:
        return hstack(x_matrix)
