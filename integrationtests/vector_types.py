from .Test import *

class TestIntegrationVectors:

    def test_octet(self):
        x = TestVariableOctet()
        x.append(10)
        x.append(16)
        x.append(100)

        data = encode_TestVariableOctet(x)
        stream = BitStream(data)
        y = decode_TestVariableOctet(stream)
        assert y[0] == 10
        assert y[1] == 16
        assert y[2] == 100

    def test_sequenceof(self):
        x = TestVariableArray()
        x.append(20)
        x.append(40)

        data = encode_TestVariableArray(x)
        stream = BitStream(data)
        y = decode_TestVariableArray(stream)
        assert y[0] == 20
        assert y[1] == 40
        