class BaseTrainerException(Exception):
    pass


class ModelDeclarationException(BaseTrainerException):
    """
    Errors in model declaration file: missing fields,
    invalid types or parameters.
    """
    pass


class ModelJsonException(ModelDeclarationException):
    """
    Model declaration parsing json file exception
    """
    pass

class ProcessingFieldException(BaseTrainerException):
    """
    Error while processing fields of the dataset.
    """
    pass

class TrainModelException(BaseTrainerException):
    """
    Exception occurs while training the model.
    """
