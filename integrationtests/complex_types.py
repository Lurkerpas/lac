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