from py0b.amount import StaticAmount, ReferenceAmount, GreedyAmount
from py0b.field import Field
from py0b.instance import Instance
from py0b.stream import Stream
from py0b.structure import Structure


class StructureField(Field):
    """
    Field for embedding Structures into Structures.
    """

    def __init__(self, structure: Structure, count: int | str = 1):
        """The provided count can be:
            - an integer in which case the provided amount is used directly
            - a string in which case it is used to reference a value from a IntegerField in the parent Structure.
            - a '*' (asterisk string) in which case 'greedy' parsing will be performed (reading will continue until the
                end of the Stream is reached)
        """
        super().__init__()
        self.structure = structure
        match count:
            case int():
                self._amount = StaticAmount(count)
            case str() if count == '*':
                self._amount = GreedyAmount()
            case str():
                self._amount = ReferenceAmount(count)
            case _:
                raise Exception("Invalid count parameter provided")

    def load(self, target: Instance, stream: Stream):
        rets = []

        if isinstance(self._amount, GreedyAmount):
            while True:
                try:
                    ret = self.structure.load(stream)
                    rets.append(ret)
                except:
                    break
        else:
            count = self._amount.resolve(target)
            for i in range(0, count):
                ret = self.structure.load(stream)
                rets.append(ret)

        if len(rets) == 1:
            setattr(target, self.name, rets[0])
        else:
            setattr(target, self.name, rets)
