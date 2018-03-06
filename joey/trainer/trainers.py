import logging


import numpy
from scipy.sparse import hstack, csc_matrix
from collections import defaultdict


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

    def _to_column(self, x):
        return numpy.transpose(
            csc_matrix([0.0 if item is None else float(item) for item in x]))


class GroupModelsTrainer(Trainer):
    pass


class PlainTrainer(Trainer):
    def train(self, iterator):
        vectorized_data, processed, ignored = self.prepare_data(iterator)
        logging.info('Processed {0} lines, ignored {1} lines'.format(processed, ignored))
        
        # Get X and y
        logging.info('Extracting fields.')
        x_matrix = []
        for name, field in self.declaration.fieldset.iteritems():
            if name == self.declaration.output_field:
                y_vector = vectorized_data[name]
            else:
                item = self.prepare_column(field, vectorized_data[name])
                if item is not None:
                    # Convert item to csc_matrix, since hstack fails with arrays
                    x_matrix.append(csc_matrix(item))

        logging.info('Training model.')
        try:
            true_data = hstack(x_matrix)
        except ValueError:
            true_data = numpy.hstack(x_matrix)

        algo = self.get_algo()
        algo.fit(true_data, [str(l) for l in y_vector])
        return algo

    def predict(self, model, iterator):
        vectorized_data, processed, ignored = self.prepare_data(
            iterator, exclude_output=True)

         # Get X and y
        logging.info('Extracting fields.')
        x_matrix = []
        for name, field in self.declaration.fieldset.iteritems():
            if name == self.declaration.output_field:
                continue
            item = self.prepare_column(field, vectorized_data[name])
            x_matrix.append(item)

        logging.info('Evaluating model.')
        if(len(x_matrix) == 1):
            predict_data = numpy.array(x_matrix[0])
        else:
            predict_data = hstack(x_matrix)

        probs = model.predict_proba(predict_data)
        result = {
            'probs': probs,
        }
        # FIXME:
        if hasattr(model, "classes_"):
            #print "!!!!!", probs, probs.argmax(axis=1)
            result["classes"] = model.classes_
            result["labels"] = model.classes_[probs.argmax(axis=1)]
        return result

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
        return vectorized_data, processed, ignored

    def prepare_column(self, field, data):
        return self._to_column(data)
