from pathlib import Path
from lac import acnencoding
from lac import lac
from lac.asn1types import \
    IntegerType, \
    RealType, \
    SequenceType, \
    ChoiceType, \
    OctetStringType, \
    SequenceOfType, \
    BooleanType, \
    EnumerationType

class TestTypes:
    __code_dir = Path(__file__).resolve().parent

    def path(self, file_name : str) -> str:
        return Path.joinpath(self.__code_dir, file_name) 

    def test_bool(self):
        modules = lac.load_modules(
            [self.path("type_boolean.asn")],
            [self.path("type_boolean.acn")],
        )
        assert 1 == len(modules)
        module = modules[0]
        assert "BooleanModule" == module.name
        assert 1 == len(module.types.values())
        type = list(module.types.values())[0]
        assert isinstance(type, BooleanType)
        assert "TestBool" == type.name

    def test_int(self):
        modules = lac.load_modules(
            [self.path("type_int.asn")],
            [self.path("type_int.acn")],
        )
        assert 1 == len(modules)
        module = modules[0]
        assert "IntModule" == module.name
        assert 1 == len(module.types.values())
        type = list(module.types.values())[0]
        assert isinstance(type, IntegerType)
        assert "TestInt" == type.name
        assert 0 == type.range.min
        assert 200 == type.range.max
        assert 8 == type.encoding.options.size.size
       
    def test_real(self):
        modules = lac.load_modules(
            [self.path("type_real.asn")],
            [self.path("type_real.acn")],
        )
        assert 1 == len(modules)
        module = modules[0]
        assert "RealModule" == module.name
        assert 1 == len(module.types.values())
        type = list(module.types.values())[0]
        assert isinstance(type, RealType)
        assert "TestReal" == type.name
        assert -2 == type.range.min
        assert 2 == type.range.max

    def test_enum(self):
        modules = lac.load_modules(
            [self.path("type_enum.asn")],
            [self.path("type_enum.acn")],
        )
        assert 1 == len(modules)
        module = modules[0]
        assert "EnumModule" == module.name
        assert 1 == len(module.types.values())
        type = list(module.types.values())[0]
        assert isinstance(type, EnumerationType)
        assert "TestEnum" == type.name
        assert 32 == type.encoding.options.size.size
        assert 3 == len(type.values)
        assert "val1" == type.values[0].name
        assert 0 == type.values[0].value
        assert "val2" == type.values[1].name
        assert 5 == type.values[1].value
        assert "val3" == type.values[2].name
        assert None == type.values[2].value

    def test_sequence(self):
        modules = lac.load_modules(
            [self.path("type_sequence.asn")],
            [self.path("type_sequence.acn")],
        )
        assert 1 == len(modules)
        module = modules[0]
        assert "SequenceModule" == module.name
        assert 2 == len(module.types.values())
        assert "TestSequence" in module.types.keys()
        type = module.types["TestSequence"]
        assert isinstance(type, SequenceType)
        assert 2 == len(type.elements)
        assert "field1" == type.elements[0].name
        assert "TestInt" == type.elements[0].type_name
        assert "field2" == type.elements[1].name
        assert "TestInt" == type.elements[1].type_name

    def test_choice(self):
        modules = lac.load_modules(
            [self.path("type_choice.asn")],
            [self.path("type_choice.acn")],
        )
        assert 1 == len(modules)
        module = modules[0]
        assert "ChoiceModule" == module.name
        assert 2 == len(module.types.values())
        assert "TestChoice" in module.types.keys()
        type = module.types["TestChoice"]
        assert isinstance(type, ChoiceType)
        assert 2 == len(type.alternatives)
        assert "field1" == type.alternatives[0].name
        assert "TestInt" == type.alternatives[0].type_name
        assert "field2" == type.alternatives[1].name
        assert "TestInt" == type.alternatives[1].type_name

    def test_octet_string(self):
        modules = lac.load_modules(
            [self.path("type_octetstring.asn")],
            [self.path("type_octetstring.acn")],
        )
        assert 1 == len(modules)
        module = modules[0]
        assert "OctetStringModule" == module.name
        assert 2 == len(module.types.values())
        assert "TestFixedOctet" in module.types.keys()
        type1 = module.types["TestFixedOctet"]
        assert isinstance(type1, OctetStringType)
        assert 8 == type1.size.size
        assert "TestVariableOctet" in module.types.keys()
        type2 = module.types["TestVariableOctet"]
        assert isinstance(type2, OctetStringType)
        assert 0 == type2.size.range.min
        assert 15 == type2.size.range.max

    def test_sequence_of(self):
        modules = lac.load_modules(
            [self.path("type_sequenceof.asn")],
            [self.path("type_sequenceof.acn")],
        )
        assert 1 == len(modules)
        module = modules[0]
        assert "SequenceOfModule" == module.name
        assert 3 == len(module.types.values())
        assert "TestFixedSequenceOf" in module.types.keys()
        type1 = module.types["TestFixedSequenceOf"]
        assert isinstance(type1, SequenceOfType)
        assert 16 == type1.size.size
        assert "TestInt" == type1.element_type_name
        assert "TestVariableSequenceOf" in module.types.keys()
        type2 = module.types["TestVariableSequenceOf"]
        assert isinstance(type2, SequenceOfType)
        assert "TestInt" == type2.element_type_name
        assert 0 == type2.size.range.min
        assert 7 == type2.size.range.max

    def test_alias(self):
        modules = lac.load_modules(
            [self.path("type_alias.asn")],
            [self.path("type_alias.acn")],
        )
        assert 1 == len(modules)
        module = modules[0]
        assert "AliasModule" == module.name
        assert 2 == len(module.types.values())
        assert "TestInt" in module.types.keys()
        type1 = module.types["TestInt"]
        assert isinstance(type1, IntegerType)
        assert 0 == type1.range.min
        assert 255 == type1.range.max
        assert "TestInt" in module.types.keys()
        type2 = module.types["TestIntAlias"]
        assert isinstance(type1, IntegerType)
        assert 17 == type2.range.min
        assert 31 == type2.range.max