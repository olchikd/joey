from base import BaseReader
from ..utils import fill_type_map

TYPE_MAP = fill_type_map(BaseReader)


class FileReaderFactory(object):
    @classmethod
    def factory(cls, file_type):
        return TYPE_MAP[file_type]()
