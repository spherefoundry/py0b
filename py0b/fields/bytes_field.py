from py0b.amount import ReferenceAmount, StaticAmount
from py0b.field import Field
from py0b.instance import Instance
from py0b.stream import Stream


class BytesField(Field):
    """Field subclass for reading a sequence of bytes."""

    def __init__(self, size: int | str):
        """The provided size can be:
            - an integer in which case the provided amount is used directly
            - a string in which case it is used to reference a value from a IntegerField in the parent Structure.
        """
        super().__init__()
        match size:
            case str():
                self._amount = ReferenceAmount(size)
            case int():
                self._amount = StaticAmount(size)

    def load(self, target: Instance, stream: Stream):
        size = self._amount.resolve(target)

        data = stream.read(size)
        setattr(target, self.name, data)
