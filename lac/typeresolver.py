from typing import List
from .asn1types import (
    Asn1Module,
    Asn1Type,
    AliasType,
    IntegerType,
    IntegerRange,
    SequenceType,
    SequenceElement,
    SequenceOfType,
    RangedSize,
    OctetStringType,
)

from .acnencoding import EncodingSpecification, EncodingOptions, DeterminedSizeEncoding

from .acntransformer import AcnModule


def get_aliased_type(alias_type: AliasType, modules: dict[str, Asn1Module]) -> Asn1Type:
    host_module = modules[alias_type.module_name]
    aliased_name = alias_type.aliased_type_name
    if aliased_name in host_module.types.keys():
        return host_module.types[aliased_name]
    importing_module = host_module.get_importing_module(aliased_name)
    if importing_module is not None:
        host_module = modules[importing_module.module_name]
        return host_module.types[aliased_name]
    return None


def resolve_int_alias(alias: AliasType, aliased_type: IntegerType) -> IntegerType:
    result = IntegerType()
    result.name = alias.name
    result.module_name = alias.name
    result.range = IntegerRange()
    result.range.min = aliased_type.range.min
    result.range.max = aliased_type.range.max
    if alias.range is not None:
        result.range.min = alias.range.min
        result.range.max = alias.range.max
    return result


def resolve_alias(alias: AliasType, aliased_type: Asn1Type) -> Asn1Type:
    match aliased_type:
        case IntegerType:
            return resolve_int_alias(alias, aliased_type)
    return None


def resolve_aliases(modules: dict[str, Asn1Module]):
    for src_module_name, src_module in modules.items():
        for type_name, type in src_module.types.items():
            if isinstance(type, AliasType):
                aliased_type = get_aliased_type(type, modules)
                if aliased_type is None:
                    raise Exception()
                new_type = resolve_alias(type, aliased_type)
                src_module.types[new_type.name] = new_type


def create_determined_sequence_of(
    asn1_module: Asn1Module,
    acn_module: AcnModule,
    base_type: SequenceOfType,
    name: str,
    determinant_name: str,
) -> SequenceOfType:
    new_type = SequenceOfType()
    new_type.module_name = asn1_module.name
    new_type.name = name
    new_type.element_type_name = base_type.element_type_name
    new_type.size = RangedSize()
    new_type.size.range.min = base_type.size.range.min
    new_type.size.range.max = base_type.size.range.max
    new_type.size.determinant_name = determinant_name
    asn1_module.types[name] = new_type
    new_type_spec = EncodingSpecification()
    new_type_spec.type_name = name
    new_type_spec.options = EncodingOptions()
    acn_module.specifications[name] = new_type_spec
    return new_type

def create_determined_octet_string(
    asn1_module: Asn1Module,
    acn_module: AcnModule,
    base_type: OctetStringType,
    name: str,
    determinant_name: str,
) -> OctetStringType:
    new_type = OctetStringType()
    new_type.module_name = asn1_module.name
    new_type.name = name
    new_type.size = RangedSize()
    new_type.size.range.min = base_type.size.range.min
    new_type.size.range.max = base_type.size.range.max
    new_type.size.determinant_name = determinant_name
    asn1_module.types[name] = new_type
    new_type_spec = EncodingSpecification()
    new_type_spec.type_name = name
    new_type_spec.options = EncodingOptions()
    acn_module.specifications[name] = new_type_spec
    return new_type

def resolve_sequence_of_determinants(
    asn1_module: Asn1Module, acn_module: AcnModule, type: SequenceType
):
    field_count = len(type.elements)
    for i in range(0, field_count):
        element = type.elements[i]
        element_type = asn1_module.types[element.type_name]
        if isinstance(element_type, SequenceOfType):
            if isinstance(element.encoding.options.size, DeterminedSizeEncoding):
                if element.encoding.options.size.determinant_name is not None:
                    new_type = create_determined_sequence_of(
                        asn1_module,
                        acn_module,
                        element_type,
                        type.name + "_" + element_type.name,
                        element.encoding.options.size.determinant_name,
                    )
                    element.type_name = new_type.name
                    element.determinant_name = element.encoding.options.size.determinant_name
        if isinstance(element_type, OctetStringType):
            if isinstance(element.encoding.options.size, DeterminedSizeEncoding):
                if element.encoding.options.size.determinant_name is not None:
                    new_type = create_determined_octet_string(
                        asn1_module,
                        acn_module,
                        element_type,
                        type.name + "_" + element_type.name,
                        element.encoding.options.size.determinant_name,
                    )
                    element.type_name = new_type.name
                    element.determinant_name = element.encoding.options.size.determinant_name


def resolve_acn_fields(type: SequenceType):
    field_count = max(len(type.elements), len(type.encoding.member_specifications))
    for i in range(0, field_count):
        element = type.elements[i]
        spec = type.encoding.member_specifications[i]
        if not spec.member_name == element.name:
            acn_element = SequenceElement()
            acn_element.acn = True
            acn_element.name = spec.member_name
            acn_element.type_name = spec.member_type_name
            acn_element.encoding = spec.specification
            type.elements.insert(i, acn_element)
        else:
            element.encoding = spec.specification


def resolve_encodings(asn1_module: Asn1Module, acn_module: AcnModule):
    input_types = asn1_module.types.copy()
    for type_name, type in input_types.items():
        if not type_name in acn_module.specifications.keys():
            continue
        acn_specification = acn_module.specifications[type_name]
        type.encoding = acn_specification
        if isinstance(type, SequenceType):
            resolve_acn_fields(type)
            resolve_sequence_of_determinants(asn1_module, acn_module, type)
