from abc import ABC, abstractmethod

from py0b.instance import Instance
from py0b.stream import Stream


class Field(ABC):
    """Base class for Fields meant to be used with Structure classes"""

    def __init__(self):
        pass

    @abstractmethod
    def load(self, target: Instance, stream: Stream):
        """Loads the related value out of the stream and stores it in the 'target' under the field 'name'.
        The amount of bytes read from the stream is specific to the type of the field and may be dynamic"""
        pass

    @property
    def name(self):
        return self._public_name

    def __get__(self, instance, owner):
        return getattr(instance, self._private_name, None)

    def __set__(self, instance, value):
        setattr(instance, self._private_name, value)

    def __set_name__(self, parent, name):
        from py0b.structure import Structure

        if not issubclass(parent, Structure):
            return
        self._public_name = name
        self._private_name = f"_{self._public_name}"
        parent.register_field(self)
