from .Test import *

class TestIntegrationDeterminants:

    def test_structure(self):
        x = Container()
        x.flag1 = True
        x.data = Container_ArrayType()
        x.data.append(10)
        x.data.append(16)
        x.data.append(7)

        data = encode_Container(x)
        stream = BitStream(data)
        y = decode_Container(stream)

        assert y.flag1 == True
        assert len(y.data) == 3
        assert y.data[0] == 10
        assert y.data[1] == 16
        assert y.data[2] == 7