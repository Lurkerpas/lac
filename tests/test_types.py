import pytest
from pathlib import Path
import lac.lac
from lac.acnencoding import *


class TestTypes:

    __code_dir = Path(__file__).resolve().parent 

    def test_ints(self):
        modules = lac.lac.load_modules(
            [Path.joinpath(self.__code_dir, "type_int.asn")],
            [Path.joinpath(self.__code_dir, "type_int.acn")])
        assert 1 == len(modules)
        module = modules[0]
        assert "IntModule" == module.name
        assert 1 == len(module.types.values())
        type = list(module.types.values())[0]
        assert "TestInt" == type.name
        assert 0 == type.range.min
        assert 200 == type.range.max
        assert 8 == type.encoding.options.size.size
        #assert IntegerEncoding.POS_INT == type.encoding.options.scalar_encoding

    def test_reals(self):
        modules = lac.lac.load_modules(
            [Path.joinpath(self.__code_dir, "type_real.asn")],
            [Path.joinpath(self.__code_dir, "type_real.acn")])
        assert 1 == len(modules)
        module = modules[0]
        assert "RealModule" == module.name
        assert 1 == len(module.types.values())
        type = list(module.types.values())[0]
        assert "TestReal" == type.name
        assert -2 == type.range.min
        assert 2 == type.range.max