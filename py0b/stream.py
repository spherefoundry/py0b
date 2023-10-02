from io import BytesIO
from typing import BinaryIO, Self


class Stream:
    """Wrapper around BinaryIO streams hiding most of its interface.

    This class can be used with a context manager, which takes case of closing the underlying BinaryIO stream"""

    def __init__(self, stream: BinaryIO):
        self._stream = stream

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    @property
    def closed(self):
        return self._stream.closed

    def close(self):
        """Closes the underlying BinaryIO stream. This method SHOULD be called before discarding instances of this
        class. The use of a context-manager is commanded"""
        self._stream.close()

    def read(self, size: int = -1) -> bytes:
        """Modifies the behaviour of 'BinaryIO.read' to raise an exception if the requested number of bytes can't be
        read from the stream."""
        data = self._stream.read(size)
        if len(data) < size:
            raise Exception("The provided stream has been consumed before providing sufficient data")
        return data

    @classmethod
    def open_file(cls, path: str) -> Self:
        """Helper method for creating a Stream using the provided file path."""
        return cls(open(path, "rb"))

    @classmethod
    def with_bytes(cls, data: bytes) -> Self:
        """Helper method for creating a Stream out of the provided bytes."""
        return cls(BytesIO(data))
