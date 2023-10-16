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


def load_modules(
    asn1_file_names: List[str], acn_file_names: List[str]
) -> List[Asn1Module]:
    asn1_parser = create_asn1_parser()
    acn_parser = create_acn_parser()

    asn1_modules = parse_asn1_modules(asn1_parser, asn1_file_names)
    acn_modules = parse_acn_modules(acn_parser, acn_file_names)

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


def save_modules(modules: dict[str, str], directory : str, extension: str):
    os.makedirs(directory, exist_ok=True)
    for module_name, module in modules.items():
        file_name = Path.joinpath(Path(directory).resolve(), f"{module_name}.{extension}")
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
    parser.add_argument(
        "-o", "--output", help="Output directory"
    )
    parser.add_argument("-v", "--verbose", help="Verbose mode")
    arguments = parser.parse_args()

    if arguments.verbose:
        __log.setLevel(level=logging.INFO)

    asn1_file_names = [
        name for name in arguments.filename if name.lower().endswith("asn")
    ]
    acn_file_names = [
        name for name in arguments.filename if name.lower().endswith("acn")
    ]
    template_file_name = arguments.template
    extension = arguments.extension
    directory = arguments.output
    input_modules = load_modules(asn1_file_names, acn_file_names)
    output_modules = process_modules(input_modules, template_file_name)
    save_modules(output_modules, directory, extension)


if __name__ == "__main__":
    main()
