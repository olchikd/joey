class Model(object):
    """
    declaration + trained algo
    """
    def __init__(self, declaration):
        self.declaration = declaration
        if declaration.group is None:
            self.trainer = PlainTrainer()
        else:
            self.trainer = GroupModelsTrainer()
