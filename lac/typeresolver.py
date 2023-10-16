from typing import List
from .asn1types import \
    Asn1Module, \
    Asn1Type, \
    AliasType, \
    IntegerType, \
    IntegerRange

from .acntransformer import AcnModule

def get_aliased_type(alias_type : AliasType, modules : dict[str, Asn1Module]) -> Asn1Type:
    host_module = modules[alias_type.module_name]
    aliased_name = alias_type.aliased_type_name
    if aliased_name in host_module.types.keys():
        return host_module.types[aliased_name]
    importing_module = host_module.get_importing_module(aliased_name)
    if importing_module is not None:
        host_module = modules[importing_module.module_name]
        return host_module.types[aliased_name]
    return None

def resolve_int_alias(alias : AliasType, aliased_type : IntegerType) -> IntegerType:
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

def resolve_alias(alias : AliasType, aliased_type : Asn1Type) -> Asn1Type:
    match aliased_type:
        case IntegerType:
            return resolve_int_alias(alias, aliased_type)
    return None

def resolve_aliases(modules : dict[str, Asn1Module]):
    for src_module_name, src_module in modules.items():
        for type_name, type in src_module.types.items():
            if isinstance(type, AliasType):
                aliased_type = get_aliased_type(type, modules)
                if aliased_type is None:
                    raise Exception()
                new_type = resolve_alias(type, aliased_type)
                src_module.types[new_type.name] = new_type
                

def resolve_encodings(asn1_module: Asn1Module, acn_module: AcnModule):
    for type_name, type in asn1_module.types.items():
        if not type_name in acn_module.specifications.keys():
            continue
        acn_specification = acn_module.specifications[type_name]
        type.encoding = acn_specification
