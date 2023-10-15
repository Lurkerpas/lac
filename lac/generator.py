from mako.template import Template
from .asn1types import *

def generate(template_file_name : str, module : Asn1Module) -> str:
    with open(template_file_name) as template_file:
        template = template_file.read()
        result = Template(template).render(module=module)
        return result
    return None 