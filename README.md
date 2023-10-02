# py0b - python binary parser framework

The aim for py0b is to provide a convenient way of reading and parsing binary files.

## Philosophy

The idea behind py0b is to provide a DSL for easy parsing of various binary formats. At the core of this DSL is the  
Structure component which serves as a container for Fields. Because Structures can also be nested inside of Structures 
(thanks to StructureField), it is possible to express a great many binary formats with a single root Structure. For 
more complex scenarios, py0b can be extended with additional logic.

### Field types

A set of field types is provided out of the box:

- IntegerField - reads integers handling endianness
- BytesField - for reading chunks of data
- StructureField - for reading nested structures

### Reference counts

Some Fields support reading multiples of the underlying type (BytesField, StructureField). This can be expressed 
directly by specifying an integer, or by referencing a different field of the same Structure. For example

```python
class CustomStructure(Structure):
    count = IntegerField.big(size=1)
    data = BytesField(size='count')
```

For StructureField it is also possible to specify 'greedy' parsing with '*' which will read as many instances of the 
structure as possible. 

```python
class InnerStructure(Structure):
    ...

class OuterStructure(Structure):
    some_field = IntegerField.big()
    other_field = IntegerField.small()
    children = StructureField(InnerStructure(), count='*')
```

## Example

To illustrate the use py0b please have a look at the `examples` directory:

- `png_info.py` - parses and prints some basic data (width, height, etc.) for the provided PNG file. All PNG chunks are read, with only IHDR being parsed further.