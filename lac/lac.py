import logging
import argparse
import os

from lark import Lark
from typing import List
from pathlib import Path

from . import asn1transformer
from . import acntransformer
from . import typeresolver
from . import generator

from .asn1types import *
from .acnencoding import *

__log = logging.getLogger("lac")
__code_dir = Path(__file__).resolve().parent


def create_asn1_parser():
    with open(Path.joinpath(__code_dir, "asn1.lark")) as asn1_grammar_file:
        asn1_grammar = asn1_grammar_file.read()
        asn1_parser = Lark(asn1_grammar, start="module")
        return asn1_parser


def create_acn_parser():
    with open(Path.joinpath(__code_dir, "acn.lark")) as acn_grammar_file:
        acn_grammar = acn_grammar_file.read()
        acn_parser = Lark(acn_grammar, start="module")
        return acn_parser


def parse_asn1_modules(
    parser: Lark, asn1_file_names: List[str]
) -> dict[str, Asn1Module]:
    modules = {}
    for file_name in asn1_file_names:
        with open(file_name) as file:
            data = file.read()
            tree = parser.parse(data)
            module = asn1transformer.parse_asn1(tree)
            modules[module.name] = module
    return modules


def parse_acn_modules(parser: Lark, acn_file_names: List[str]) -> dict[str, AcnModule]:
    modules = {}
    for file_name in acn_file_names:
        with open(file_name) as file:
            data = file.read()
            tree = parser.parse(data)
            module = acntransformer.parse_acn(tree)
            modules[module.name] = module
    return modules


def resolve_encodings(
    asn1_modules: dict[str, Asn1Module], acn_modules: dict[str, AcnModule]
) -> None:
    for asn1_module in asn1_modules.values():
        name = asn1_module.name
        if not name in acn_modules.keys():
            raise Exception()
        acn_module = acn_modules[name]
        typeresolver.resolve_encodings(asn1_module, acn_module)

def resolve_imports(
    asn1_modules: dict[str, Asn1Module]
) -> None:
    for asn1_module in asn1_modules.values():
        for import_declaration in asn1_module.imports:
            other_module = asn1_modules[import_declaration.module_name]
            for other_type_name in import_declaration.type_names:
                other_type = other_module.types[other_type_name]
                asn1_module.imported_types[other_type_name] = other_type


def load_modules(
    asn1_file_names: List[str], acn_file_names: List[str]
) -> List[Asn1Module]:
    asn1_parser = create_asn1_parser()
    acn_parser = create_acn_parser()

    asn1_modules = parse_asn1_modules(asn1_parser, asn1_file_names)
    acn_modules = parse_acn_modules(acn_parser, acn_file_names)

    resolve_imports(asn1_modules)
    resolve_encodings(asn1_modules, acn_modules)
    typeresolver.resolve_aliases(asn1_modules)
    return list(asn1_modules.values())


def process_modules(
    asn1_modules: List[Asn1Module], template_file_name: str
) -> dict[str, str]:
    result = {}
    for asn1_module in asn1_modules:
        data = generator.generate(template_file_name, asn1_module)
        result[asn1_module.name] = data
    return result


def add_structure_members(asn1_module : Asn1Module, elements : List[SequenceElement], sequence : SequenceType):
    for element in sequence.elements:
        type_name = element.type_name
        type = asn1_module.types[type_name] if type_name in asn1_module.types.keys() \
            else asn1_module.imported_types[type_name] if type_name in asn1_module.imported_types.keys() \
                else None
        if type is not None and isinstance(type, SequenceType):
            add_structure_members(asn1_module, elements, type)
        else:
            elements.append(element)


def flatten_structure(asn1_module : Asn1Module, sequence : SequenceType):
    members = []
    add_structure_members(asn1_module, members, sequence)
    sequence.elements = members


def flatten_structures(asn1_modules: List[Asn1Module]):
    for asn1_module in asn1_modules:
        for _, asn1_type in asn1_module.types.items():
            if isinstance(asn1_type, SequenceType):
                flatten_structure(asn1_module, asn1_type)


def save_modules(modules: dict[str, str], directory: str, extension: str):
    os.makedirs(directory, exist_ok=True)
    for module_name, module in modules.items():
        file_name = Path.joinpath(
            Path(directory).resolve(), f"{module_name}.{extension}"
        )
        with open(file_name, "w") as file:
            file.write(module)


def main():
    logging.basicConfig(level=logging.WARNING)
    parser = argparse.ArgumentParser(prog="LAC", description="Light ASN.1 Compiler")
    parser.add_argument(
        "filename",
        nargs="+",
        help="List of files to parse. Each ASN.1 module shall be matched by the corresponding ACN module",
    )
    parser.add_argument(
        "-t", "--template", help="Template file used to process ASN.1/ACN data"
    )
    parser.add_argument(
        "-e", "--extension", help="Extension to be used for the output files"
    )
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument("-v", "--verbose", help="Verbose mode", action='store_true')
    parser.add_argument("-fs", "--flattenstructures", help="Flatten structures", action='store_true')
    arguments = parser.parse_args()

    if arguments.verbose:
        __log.setLevel(level=logging.INFO)

    asn1_file_names = [
        name for name in arguments.filename if name.lower().endswith("asn") or name.lower().endswith("asn1") 
    ]
    acn_file_names = [
        name for name in arguments.filename if name.lower().endswith("acn")
    ]
    template_file_name = arguments.template
    extension = arguments.extension
    directory = arguments.output
    input_modules = load_modules(asn1_file_names, acn_file_names)
    if arguments.flattenstructures:
        flatten_structures(input_modules)
    output_modules = process_modules(input_modules, template_file_name)
    save_modules(output_modules, directory, extension)


if __name__ == "__main__":
    main()
