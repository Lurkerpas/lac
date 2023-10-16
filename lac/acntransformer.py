from typing import List
from lark import ParseTree, Token, Tree
from .acnencoding import (
    AcnModule,
    SizeEncoding,
    FixedSizeEncoding,
    DeterminedSizeEncoding,
    Endianness,
    ScalarEncoding,
    IntegerEncoding,
    FloatEncoding,
    MemberEncodingSpecification,
    EncodingSpecification,
    EncodingOptions,
)


def parse_acn_integer_value(tree: ParseTree) -> int:
    return int(tree.children[0].value)


def parse_acn_size_encoding(tree: ParseTree) -> SizeEncoding:
    if tree.children[0].data.value == "integer_value":
        size = FixedSizeEncoding()
        size.size = parse_acn_integer_value(tree.children[0])
        return size
    else:
        pass


def parse_acn_encoding_options(tree: ParseTree) -> EncodingOptions:
    options = EncodingOptions()
    for child in tree.children:
        if len(child.children) > 0 and child.children[0] is not None:
            match child.children[0].data.value:
                case "size_specification":
                    options.size = parse_acn_size_encoding(child.children[0])
                case _:
                    pass
    return options

def parse_acn_member_encoding_specification(tree: ParseTree) -> MemberEncodingSpecification:
    spec = MemberEncodingSpecification()
    spec.member_name = tree.children[0].value
    spec.member_type_name = None
    if tree.children[1] is not None:
        spec.member_type_name = tree.children[1].value
    spec.specification # TODO
    return spec
    

def parse_acn_encoding_specification(tree: ParseTree) -> EncodingSpecification:
    result = EncodingSpecification()
    result.type_name = tree.children[0].value
    result.options = parse_acn_encoding_options(tree.children[1].children[0])

    for i in range(1,len(tree.children[1].children)):
        child = tree.children[1].children[i]
        if child is not None:
            spec = parse_acn_member_encoding_specification(child)
            result.member_specifications.append(spec)

    return result


def parse_acn_module_body(tree: ParseTree) -> dict[str, EncodingSpecification]:
    result = {}
    for child in tree.children:
        spec = parse_acn_encoding_specification(child)
        result[spec.type_name] = spec
    return result


def parse_acn_module(tree: ParseTree) -> AcnModule:
    module = AcnModule()
    for child in tree.children:
        if isinstance(child, Token):
            module.name = child.value
        elif isinstance(child, Tree):
            match child.data.value:
                case "module_body":
                    module.specifications = parse_acn_module_body(child)
                case _:
                    pass
    return module


def parse_acn(tree: ParseTree) -> AcnModule:
    data = tree.data
    if isinstance(data, Token):
        match data.value:
            case "module":
                return parse_acn_module(tree)
            case _:
                pass
