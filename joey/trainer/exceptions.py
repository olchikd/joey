class BaseTrainerException(Exception):
    pass


class ModelDeclarationException(BaseTrainerException):
    pass


class ModelJsonException(ModelDeclarationException):
    pass


class ParsingException(BaseTrainerException):
    pass


class ProcessingException(BaseTrainerException):
    pass
