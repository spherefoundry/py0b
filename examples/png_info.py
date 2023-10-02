from enum import IntEnum

from py0b import Structure, Stream, Instance

from py0b.fields import BytesField, IntegerField, StructureField


class PNGColorType(IntEnum):
    GREYSCALE = 0
    TRUECOLOR = 2
    INDEXED = 3
    GREYSCALE_WITH_ALPHA = 4
    TRUECOLOR_WITH_ALPHA = 6

    @property
    def description(self) -> str:
        match self:
            case PNGColorType.GREYSCALE:
                return "Grayscale"
            case PNGColorType.TRUECOLOR:
                return "Truecolor"
            case PNGColorType.INDEXED:
                return "Indexed"
            case PNGColorType.GREYSCALE_WITH_ALPHA:
                return "Grayscale (with Alpha)"
            case PNGColorType.TRUECOLOR_WITH_ALPHA:
                return "Truecolor (with Alpha)"
            case _:
                raise Exception("Invalid value for PNGColorType")


class PNGInterlaceMethod(IntEnum):
    NONE = 0
    ADAM7 = 1

    @property
    def description(self) -> str:
        match self:
            case PNGInterlaceMethod.NONE:
                return "None"
            case PNGInterlaceMethod.ADAM7:
                return "Adam7"
            case _:
                raise Exception("Invalid value for PNGInterlaceMethod")


class PNGHeader(Structure):
    file_signature = BytesField(size=8)

    def post_process(self, candidate: Instance):
        if candidate.file_signature != b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a':
            raise Exception("The provided file has a non-PNG file signature")


# Specification: http://libpng.org/pub/png/spec/iso/index-object.html#11IHDR
class PNGIHDR(Structure):
    width = IntegerField.big()
    height = IntegerField.big()
    bit_depth = IntegerField.big(size=1)
    colour_type = IntegerField.big(size=1)
    compression_method = IntegerField.big(size=1)
    filter_method = IntegerField.big(size=1)
    interlace_method = IntegerField.big(size=1)

    def post_process(self, candidate: Instance):
        candidate.colour_type = PNGColorType(candidate.colour_type)
        candidate.interlace_method = PNGInterlaceMethod(candidate.interlace_method)


# http://libpng.org/pub/png/spec/iso/index-object.html#5DataRep
class PNGChunk(Structure):
    length = IntegerField.big()
    type = BytesField(size=4)
    data = BytesField(size='length')
    crc = BytesField(size=4)

    def post_process(self, candidate: Instance):
        data_stream = Stream.with_bytes(candidate.data)

        # Note: Processing for more chunk parts could be added here
        match candidate.type:
            case b'IHDR':
                candidate.value = PNGIHDR().load(data_stream)

        del candidate.data


# http://libpng.org/pub/png/spec/iso/index-object.html
class PNG(Structure):
    header = StructureField(structure=PNGHeader())
    chunks = StructureField(structure=PNGChunk(), count='*')


if __name__ == '__main__':
    from argparse import ArgumentParser
    import os

    parser = ArgumentParser(
        prog='png_info',
        description='Display basic information about the provided PNG file'
    )
    parser.add_argument('path', type=str, help="location of the input file")

    args = parser.parse_args()
    path = args.path
    path = os.path.abspath(path)

    with Stream.open_file(path) as stream:
        png_loader = PNG()
        png = png_loader.load(stream)

        ihdr = next((x.value for x in png.chunks if x.type == b'IHDR'), None)
        print(f"Width: {ihdr.width}")
        print(f"Height: {ihdr.height}")
        print(f"Bit depth: {ihdr.bit_depth}")
        print(f"Colour type: {ihdr.colour_type.description}")
        print(f"Interlace method: {ihdr.interlace_method.description}")
