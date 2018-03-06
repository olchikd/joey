from trainers import PlainTrainer, GroupModelsTrainer


class Model(object):
    """
    declaration + trained algo
    """
    def __init__(self, declaration):
        self.declaration = declaration
        self.trained_model = None
        if declaration.group is None:
            self.trainer = PlainTrainer(declaration)
        else:
            self.trainer = GroupModelsTrainer(declaration)

    def train(self, iterator):
        self.trained_model = self.trainer.train(iterator)

    def predict(self, iterator):
        return self.trainer.predict(self.trained_model, iterator)
