from typing import List
from enum import Enum
from .acnencoding import EncodingSpecification


class IntegerRange:
    min: int
    max: int

    def __init__(self) -> None:
        self.min = 0
        self.max = 0


class Size:
    pass


class FixedSize(Size):
    size: int

    def __init__(self) -> None:
        super().__init__()
        self.size = 0


class RangedSize(Size):
    range: IntegerRange
    determinant_name: str

    def __init__(self) -> None:
        super().__init__()
        self.determinant_name = None
        self.range = IntegerRange()


class RealRange:
    min: float
    max: float

    def __init__(self) -> None:
        self.min = 0.0
        self.max = 0.0


class Asn1Type:
    module_name: str
    name: str
    size: Size
    encoding: EncodingSpecification

    def __init__(self) -> None:
        self.module_name = None
        self.name = ""
        self.size = None


class IntegerType(Asn1Type):
    range: IntegerRange

    def __init__(self) -> None:
        super().__init__()
        self.range = None


class RealType(Asn1Type):
    range: RealRange

    def __init__(self) -> None:
        super().__init__()
        self.range = None


class BooleanType(Asn1Type):
    def __init__(self) -> None:
        super().__init__()


class EnumerationValue:
    name: str
    value: int

    def __init__(self) -> None:
        self.name = ""
        self.value = None


class EnumerationType(Asn1Type):
    values: List[EnumerationValue]
    encode_values: bool

    def __init__(self) -> None:
        super().__init__()
        self.values = []
        self.encode_values = False


class SequenceElement:
    name: str
    type_name: str
    optional: bool
    acn: bool
    determinant_name: str
    determined_member_name: str
    encoding: EncodingSpecification

    def __init__(self) -> None:
        self.name = ""
        self.type_name = ""
        self.optional = False
        self.acn = False
        self.encoding = None
        self.determinant_name = None
        self.determined_member_name = None


class SequenceType(Asn1Type):
    elements: List[SequenceElement]

    def __init__(self) -> None:
        super().__init__()
        self.elements = []


class ChoiceAlternative:
    name: str
    type_name: str

    def __init__(self) -> None:
        self.name = ""
        self.type_name = ""


class ChoiceType(Asn1Type):
    alternatives: List[ChoiceAlternative]

    def __init__(self) -> None:
        super().__init__()
        self.alternatives = []


class SequenceOfType(Asn1Type):
    element_type_name: str
    size: Size

    def __init__(self) -> None:
        super().__init__()
        self.element_type_name = ""
        self.size = None


class OctetStringType(Asn1Type):
    size: Size

    def __init__(self) -> None:
        super().__init__()
        self.size = None


class Ia5StringType(Asn1Type):
    size: Size

    def __init__(self) -> None:
        super().__init__()
        self.size = None


class BitStringType(Asn1Type):
    size: Size

    def __init__(self) -> None:
        super().__init__()
        self.size = None


class AliasType(Asn1Type):
    aliased_type_name: str

    def __init__(self) -> None:
        super().__init__()
        self.aliased_type_name = ""


class NullType(Asn1Type):
    def __init__(self) -> None:
        super().__init__()


class ModuleImport:
    module_name: str
    type_names: set[str]

    def __init__(self) -> None:
        self.module_name = ""
        self.type_names = set()


class Asn1Module:
    name: str
    imports: List[ModuleImport]
    imported_types : dict[str, Asn1Type]
    types: dict[str, Asn1Type]

    def get_importing_module(self, type_name: str) -> ModuleImport:
        for module_import in self.imports:
            if type_name in module_import.type_names:
                return module_import
        return None

    def __init__(self) -> None:
        self.name = ""
        self.imports = []
        self.types = {}
        self.imported_types = {}
