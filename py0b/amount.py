from abc import ABC, abstractmethod

from py0b.instance import Instance


class Amount(ABC):
    """Base class for specifying amounts. Useful when declaring size/count for various types of fields."""

    @abstractmethod
    def resolve(self, target: Instance) -> int:
        """Return the amount value at the moment of the call. Subclasses may query the provided target to establish
        the desired value."""
        pass


class StaticAmount(Amount):
    """Simple Amount subclass always returning the value provided during construction."""

    def __init__(self, count: int):
        self._count = count

    def resolve(self, target: Instance) -> int:
        return self._count


class ReferenceAmount(Amount):
    """Amount subclass that references a value from a different field. The referenced field needs to be 'before' the
        usage of this amount.
    """

    def __init__(self, field_name: str):
        self._field_name = field_name

    def resolve(self, target: Instance) -> int:
        value = getattr(target, self._field_name, None)

        if value is None:
            raise Exception(
                f'Reference amount resolution failed. The parent structure has no field named {self._field_name}'
            )

        if not isinstance(value, int):
            raise Exception(
                f'Reference amount resolution failed. The parent structure field named {self._field_name} should be '
                f'an integer type'
            )

        return value


class GreedyAmount(Amount):
    """Special subclass of Amount signifying that as many values as possible should be parsed. Calling the 'resolve'
    method will raise an exception"""

    def resolve(self, target: Instance) -> int:
        raise Exception(
            "Greedy amount must be resolved externally"
        )
