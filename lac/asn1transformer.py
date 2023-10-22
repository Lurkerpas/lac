from typing import List
from lark import ParseTree, Token, Tree
from .asn1types import (
    Asn1Module,
    ModuleImport,
    Asn1Type,
    IntegerType,
    IntegerRange,
    RealRange,
    RealType,
    BooleanType,
    EnumerationValue,
    EnumerationType,
    SequenceElement,
    SequenceType,
    ChoiceAlternative,
    ChoiceType,
    SequenceOfType,
    OctetStringType,
    Ia5StringType,
    BitStringType,
    AliasType,
    Size,
    RangedSize,
    FixedSize,
    NullType,
)


def parse_asn1_module_import(tree: ParseTree) -> ModuleImport:
    result = ModuleImport()
    for child in tree.children:
        if isinstance(child, Token):
            match child.type:
                case "TYPE_IDENTIFIER":
                    result.type_names.add(child.value)
                case "MODULE_IDENTIFIER":
                    result.module_name = child.value
    return result


def parse_asn1_module_imports(tree: ParseTree) -> List[ModuleImport]:
    result = []
    for child in tree.children:
        if isinstance(child, Tree):
            match child.data.value:
                case "import_statement":
                    result.append(parse_asn1_module_import(child))
                case _:
                    pass
    return result


def parse_asn1_integer_value(tree: ParseTree) -> int:
    if tree.data.value == "integer_value":
        return int(tree.children[0].value)
    pass


def parse_asn1_real_value(tree: ParseTree) -> int:
    if tree.data.value == "real_value":
        return float(tree.children[0].value)
    pass


def parse_asn1_integer_range(tree: ParseTree) -> IntegerRange:
    range = IntegerRange()
    range.min = parse_asn1_integer_value(tree.children[0])
    range.max = parse_asn1_integer_value(tree.children[1])
    return range


def parse_asn1_real_range(tree: ParseTree) -> RealRange:
    range = RealRange()
    range.min = parse_asn1_real_value(tree.children[0])
    range.max = parse_asn1_real_value(tree.children[1])
    return range


def parse_asn1_integer_definition(tree: ParseTree) -> IntegerType:
    result = IntegerType()
    result.range = parse_asn1_integer_range(tree)
    return result


def parse_asn1_real_definition(tree: ParseTree) -> RealType:
    result = RealType()
    result.range = parse_asn1_real_range(tree)
    return result


def parse_asn1_bool_definition(tree: ParseTree) -> BooleanType:
    result = BooleanType()
    return result


def parse_asn1_enum_value(tree: ParseTree) -> EnumerationValue:
    value = EnumerationValue()
    value.name = tree.children[0].value
    if isinstance(tree.children[1], Tree):
        value.value = parse_asn1_integer_value(tree.children[1])
    return value


def parse_asn1_enum_definition(tree: ParseTree) -> EnumerationType:
    result = EnumerationType()
    for child in tree.children:
        result.values.append(parse_asn1_enum_value(child))
    return result


def parse_asn1_choice_alternative(tree: ParseTree) -> ChoiceAlternative:
    result = ChoiceAlternative()
    result.name = tree.children[0].value
    result.type_name = tree.children[1].value
    return result


def parse_asn1_choice_definition(tree: ParseTree) -> ChoiceType:
    result = ChoiceType()
    for child in tree.children:
        result.alternatives.append(parse_asn1_choice_alternative(child))
    return result


def parse_asn1_sequence_element(tree: ParseTree) -> SequenceElement:
    result = SequenceElement()
    result.name = tree.children[0].value
    result.type_name = tree.children[1].value
    if isinstance(tree.children[2], Tree):
        pass  # TODO
    return result


def parse_asn1_sequence_definition(tree: ParseTree) -> SequenceType:
    result = SequenceType()
    for child in tree.children:
        result.elements.append(parse_asn1_sequence_element(child))
    return result


def parse_asn1_size_definition(tree: ParseTree) -> Size:
    match len(tree.children):
        case 1:
            size = FixedSize()
            size.size = parse_asn1_integer_value(tree.children[0])
            return size
        case 2:
            size = RangedSize()
            size.range = IntegerRange()
            size.range.min = parse_asn1_integer_value(tree.children[0])
            size.range.max = parse_asn1_integer_value(tree.children[1])
            return size
        case _:
            pass


def parse_asn1_sequence_of_definition(tree: ParseTree) -> SequenceOfType:
    result = SequenceOfType()
    result.size = parse_asn1_size_definition(tree.children[0])
    result.element_type_name = tree.children[1].value
    return result


def parse_asn1_bitstring_definition(tree: ParseTree) -> BitStringType:
    result = BitStringType()
    result.size = parse_asn1_size_definition(tree.children[0])
    return result


def parse_asn1_octetstring_definition(tree: ParseTree) -> OctetStringType:
    result = OctetStringType()
    result.size = parse_asn1_size_definition(tree.children[0])
    return result


def parse_asn1_ia5string_definition(tree: ParseTree) -> Ia5StringType:
    result = Ia5StringType()
    result.size = parse_asn1_size_definition(tree.children[0])
    return result


def parse_asn1_alias_definition(tree: ParseTree) -> AliasType:
    result = AliasType()
    result.aliased_type_name = tree.children[0].value
    if len(tree.children) == 3:
        if isinstance(tree.children[1], Tree) and isinstance(tree.children[2], Tree):
            result.range = IntegerRange()
            result.range.min = parse_asn1_integer_value(tree.children[1])
            result.range.max = parse_asn1_integer_value(tree.children[2])
    return result


def parse_asn1_null_definition(tree: ParseTree) -> NullType:
    result = NullType()
    return result


def parse_asn1_type_definition(tree: ParseTree) -> Asn1Type:
    name = ""
    type = None
    for child in tree.children:
        if isinstance(child, Token):
            name = child.value
        elif isinstance(child, Tree):
            match child.data.value:
                case "integer_definition":
                    type = parse_asn1_integer_definition(child)
                case "real_definition":
                    type = parse_asn1_real_definition(child)
                case "boolean_definition":
                    type = parse_asn1_bool_definition(child)
                case "enumeration_definition":
                    type = parse_asn1_enum_definition(child)
                case "alias_definition":
                    type = parse_asn1_alias_definition(child)
                case "sequence_definition":
                    type = parse_asn1_sequence_definition(child)
                case "sequence_of_definition":
                    type = parse_asn1_sequence_of_definition(child)
                case "choice_definition":
                    type = parse_asn1_choice_definition(child)
                case "octetstring_definition":
                    type = parse_asn1_octetstring_definition(child)
                case "bitstring_definition":
                    type = parse_asn1_bitstring_definition(child)
                case "ia5string_definition":
                    type = parse_asn1_ia5string_definition(child)
                case "null_definition":
                    type = parse_asn1_null_definition(child)
                case _:
                    pass
    type.name = name
    return type


def parse_asn1_module_body(tree: ParseTree) -> dict[str, Asn1Type]:
    result = {}
    for child in tree.children:
        if isinstance(child, Tree):
            match child.data.value:
                case "type_definition":
                    type = parse_asn1_type_definition(child)
                    result[type.name] = type
                case _:
                    pass
    return result


def parse_asn1_module(tree: ParseTree) -> Asn1Module:
    module = Asn1Module()
    for child in tree.children:
        if isinstance(child, Token):
            module.name = child.value
        elif isinstance(child, Tree):
            match child.data.value:
                case "module_imports":
                    module.imports = parse_asn1_module_imports(child)
                case "module_body":
                    module.types = parse_asn1_module_body(child)
                case _:
                    pass
    for _, type in module.types.items():
        type.module_name = module.name
    return module


def parse_asn1(tree: ParseTree) -> Asn1Module:
    data = tree.data
    if isinstance(data, Token):
        match data.value:
            case "module":
                return parse_asn1_module(tree)
            case _:
                pass
