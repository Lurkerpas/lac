from typing import List
from enum import Enum


class SizeEncoding:
    pass


class FixedSizeEncoding(SizeEncoding):
    size: int


class DeterminedSizeEncoding(SizeEncoding):
    determinant_name: str


class Endianness(Enum):
    BIG = 0
    LITTLE = 1


class ScalarEncoding(Enum):
    pass


class IntegerEncoding(ScalarEncoding):
    POS_INT = 0
    TWOS_COMPLEMENT = 1


class FloatEncoding(ScalarEncoding):
    IEEE_32 = 0
    IEEE_64 = 1


class MemberEncodingSpecification:
    member_name: str
    specification: "EncodingSpecification"

    def __init__(self) -> None:
        self.member_name = ""


class EncodingOptions:
    presence_condition: str  # TODO
    encode_values: bool
    size: SizeEncoding
    endianness: Endianness
    scalar_encoding: ScalarEncoding


class EncodingSpecification:
    type_name: str
    options: EncodingOptions
    member_specifications: List[MemberEncodingSpecification]

    def __init__(self) -> None:
        self.member_specifications = []
        self.type_name = ""


class AcnModule:
    name: str
    specifications: dict[str, EncodingSpecification]

    def __init__(self) -> None:
        self.name = ""
        self.specifications = {}