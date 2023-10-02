from py0b.field import Field
from py0b.instance import Instance
from py0b.stream import Stream


class Structure:
    """Container for Fields"""
    def load(self, stream: Stream) -> Instance:
        """Loads field out of the provided Stream and stores them into the returned Instance. """
        ret = Instance()
        for field in self.collected_fields:
            field.load(ret, stream)

        self.post_process(ret)

        return ret

    def post_process(self, candidate: Instance):
        """Called after load is finished reading all fields. Should be used for further processing and
        refinement of the to-be returned data."""
        pass

    @property
    def collected_fields(self) -> [Field]:
        """Returns the list of registered field instances"""
        return getattr(self.__class__, "_collected_fields", [])

    @classmethod
    def register_field(cls, field: Field):
        """Register an additional field into the structure. Used by Fields internally."""
        collected_fields = getattr(cls, "_collected_fields", [])
        collected_fields.append(field)
        setattr(cls, "_collected_fields", collected_fields)
