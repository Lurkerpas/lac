from .Test import *

class TestIntegrationComplexTypes:

    def test_structure(self):
        x = TestStructure()
        x.field1 = 16
        x.field2 = 2.0

        data = encode_TestStructure(x)
        stream = BitStream(data)
        y = decode_TestStructure(stream)
        assert y.field1 == 16
        assert y.field2 == 2.0

    def test_union(self):
        x = TestUnion()
        x.kind = TestUnion_selection.alt2_PRESENT
        x.u = 0.5

        data = encode_TestUnion(x)
        stream = BitStream(data)
        y = decode_TestUnion(stream)
        assert y.kind == TestUnion_selection.alt2_PRESENT
        assert y.u == 0.5

    def test_nested_structure(self):
        x = NestedStructure()
        struct = TestStructure()
        struct.field1 = 32
        struct.field2 = 1.0
        x.innerStruct = struct
        x.innerUnion = TestUnion()
        x.innerUnion.kind = TestUnion_selection.alt1_PRESENT
        x.innerUnion.u = 32.0
        x.param1 = 24

        data = encode_NestedStructure(x)
        stream = BitStream(data)
        y = decode_NestedStructure(stream)
        assert y.innerStruct.field1 == 32
        assert y.innerStruct.field2 == 1.0
        assert y.innerUnion.kind == TestUnion_selection.alt1_PRESENT
        assert y.innerUnion.u == 32.0
        assert y.param1 == 24