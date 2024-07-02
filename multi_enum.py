from enum import StrEnum


class MultiEnum(StrEnum):

    def __init_subclass__(cls, **kwargs):
        for enum in cls:
            main, other = kwargs.get("main"), kwargs.get("other")
            attrs = set()
            if main:
                setattr(enum, main, enum._value_)
            for attr, arg in zip(other, enum._args_):
                setattr(enum, attr, arg)
            cls._attrs_ = {main or "_value_", *other}
            delattr(enum, "_args_")

    def __new__(cls, value, *args):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._args_ = args

        return obj

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if any(getattr(member, attr) == value for attr in cls._attrs_):
                return member
        return None

    def __repr__(self):
        return f"({self.__class__}: {', '.join('='.join((attr, getattr(self, attr))) for attr in self._attrs_)})"


class Dupa(MultiEnum, main="country", other=("capital", "language", "currency")):
    poland = "Poland", "Warsaw", "Polish", "PLN"
    france = "France", "Paris", "French", "EUR"


print(repr(Dupa("EUR")))
print(Dupa.poland.currency)
