class DataType:
    @classmethod
    def all(cls):
        return [getattr(cls, k) for k in dir(cls) if k.isupper()]

class LinkPrecedenceTypes(DataType):
    SECONDARY = 'secondary'
    PRIMARY = 'primary'