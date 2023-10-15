from typing import List
from .asn1types import Asn1Module, Asn1Type
from .acntransformer import AcnModule


def resolve_encodings(asn1_module: Asn1Module, acn_module: AcnModule):
    for type_name, type in asn1_module.types.items():
        if not type_name in acn_module.specifications.keys():
            continue
        acn_specification = acn_module.specifications[type_name]
        type.encoding = acn_specification
