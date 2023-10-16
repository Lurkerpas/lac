## Python includes for Python code
<%
from lac.asn1types import \
    IntegerType, \
    RealType, \
    BooleanType, \
    EnumerationType, \
    SequenceType, \
    SequenceOfType, \
    ChoiceType, \
    OctetStringType
%>
## Python definitions
<%
module_name = module.name.upper()
%>
## Standard Python imports
from typing import List, Union
from enum import Enum
from bitstring import Bits, BitArray, BitStream, pack

## Includes for imported types
% for include in module.imports:
from .${include.module_name} import *
% endfor

## Type declarations
% for type in module.types.values():
## IntegerType
% if isinstance(type, IntegerType):
${type.name} = int
% endif
## RealType
% if isinstance(type, RealType):
${type.name} = float
% endif
## BooleanType
% if isinstance(type, BooleanType):
${type.name} = bool
% endif
## EnumerationType
% if isinstance(type, EnumerationType):
class ${type.name}(Enum): 
% for value in type.values:
%   if value.value is not None:
    ${value.name.upper()} = ${value.value},
%   else:
    ${value.name.upper()},
%   endif
% endfor


% endif
## SequenceType
% if isinstance(type, SequenceType):
class ${type.name}:
% for member in type.elements:
    ${member.name} : ${member.type_name}
% endfor


% endif
## ChoiceType
% if isinstance(type, ChoiceType):
${type.name} = Union[
% for member in type.alternatives:
        ${member.type_name},
% endfor
    ]

% endif
% endfor

## Type transcoding
% for type in module.types.values():
## IntegerType
% if isinstance(type, IntegerType):
def encode_${type.name}(x : ${type.name}) -> BitArray:
    return BitArray(int=x, length=${type.encoding.options.size.size})

def decode_${type.name}(data : BitStream) -> ${type.name}:
    x = data[data.bitpos:data.bitpos+${type.encoding.options.size.size}].int
    data.bitpos += ${type.encoding.options.size.size}
    return x

% endif
## RealType
% if isinstance(type, RealType):
def encode_${type.name}(x : ${type.name}) -> BitArray:
    data = BitArray()
    data.f32 = x
    return data

def decode_${type.name}(data : BitStream) -> ${type.name}:
    x = data[data.bitpos:data.bitpos+32].f32
    data.bitpos += 32
    return x

% endif
## BooleanType
% if isinstance(type, BooleanType):

% endif
## EnumerationType
% if isinstance(type, EnumerationType):
% for value in type.values:

% endfor
% endif
## SequenceType
% if isinstance(type, SequenceType):
def encode_${type.name}(x : ${type.name}) -> BitArray:
    data = BitArray()
% for member in type.elements:
    data = data + encode_${member.type_name}(x.${member.name})
% endfor
    return data

def decode_${type.name}(data : BitStream) -> ${type.name}:
    x = ${type.name}()
% for member in type.elements:
    x.${member.name} = decode_${member.type_name}(data)
% endfor
    return x

% endif
## ChoiceType
% if isinstance(type, ChoiceType):
% for member in type.alternatives:
% endfor
% endif
% endfor
