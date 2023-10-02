from py0b.amount import StaticAmount, ReferenceAmount, GreedyAmount
from py0b.field import Field
from py0b.instance import Instance
from py0b.stream import Stream
from py0b.structure import Structure


class StructureField(Field):
    """"""

    def __init__(self, structure: Structure, count: int | str = 1):
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
