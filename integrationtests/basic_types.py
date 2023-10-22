from .Test import *

class TestIntegrationBasicTypes:

    def test_int(self):
        x = 7

        data = encode_UInt8(x)
        stream = BitStream(data)
        y = decode_UInt8(stream)
        assert y == 7

    def test_float(self):
        x = 0.25

        data = encode_Float32(x)
        stream = BitStream(data)
        y = decode_Float32(stream)
        assert y == 0.25

    def test_enum(self):
        x = Values.VAL3

        data = encode_Values(x)
        stream = BitStream(data)
        y = decode_Values(stream)
        assert y == Values.VAL3

    def test_bool(self):
        x1 = True
        x2 = False

        data = encode_Bool8(x1) + encode_Bool8(x2) 
        stream = BitStream(data)
        y1 = decode_Bool8(stream)
        y2 = decode_Bool8(stream)
        assert y1 == True
        assert y2 == False
