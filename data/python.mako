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
    OctetStringType, \
    RangedSize
%>
## Python definitions
<%
module_name = module.name.upper()
%>
## Standard Python imports
from typing import List, Union
from enum import Enum, IntEnum
from bitstring import BitArray, BitStream

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
class ${type.name}(IntEnum): 
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
% if not member.acn:
    ${member.name} : '${member.type_name}'
% endif
% endfor


% endif
## ChoiceType
% if isinstance(type, ChoiceType):
class ${type.name}_selection(IntEnum):
<% count = 0 %>\
% for member in type.alternatives:
    ${member.name}_PRESENT = ${count}, <% count = count + 1 %>
% endfor

${type.name}_union = Union[
% for member in type.alternatives:
        ${member.type_name},
% endfor
    ]

class ${type.name}:
    kind : ${type.name}_selection
    u : ${type.name}_union


%endif
## OctetStringType
% if isinstance(type, OctetStringType):
${type.name} = bytearray

% endif
## SequenceOfType
% if isinstance(type, SequenceOfType):
${type.name} = list[${type.element_type_name}]

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
def encode_${type.name}(x : ${type.name}) -> BitArray:
    value = 1 if x else 0
    return BitArray(uint=value, length=${type.encoding.options.size.size})

def decode_${type.name}(data : BitStream) -> ${type.name}:
    value = data[data.bitpos:data.bitpos+${type.encoding.options.size.size}].uint
    data.bitpos += ${type.encoding.options.size.size}
    return value != 0

% endif
## EnumerationType
% if isinstance(type, EnumerationType):
def encode_${type.name}(x : ${type.name}) -> BitArray:
    return BitArray(uint=x, length=${type.encoding.options.size.size})

def decode_${type.name}(data : BitStream) -> ${type.name}:
    x = data[data.bitpos:data.bitpos+${type.encoding.options.size.size}].uint
    data.bitpos += ${type.encoding.options.size.size}
    return ${type.name}(x)

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
%   if member.acn:
    ${member.name} = decode_${member.type_name}(data)
%   else:
%       if member.determinant_name is not None:
    x.${member.name} = decode_${member.type_name}(${member.determinant_name}, data)
%       else:
    x.${member.name} = decode_${member.type_name}(data)
%       endif
%   endif
% endfor
    return x

% endif
## ChoiceType
% if isinstance(type, ChoiceType):
def encode_${type.name}_selection(x : ${type.name}_selection) -> BitArray:
    return BitArray(int=x, length=8)

def decode_${type.name}_selection(data : BitStream) -> ${type.name}_selection:
    x = data[data.bitpos:data.bitpos+8].int
    data.bitpos += 8
    return x

def encode_${type.name}(x : ${type.name}) -> BitArray:
    data = encode_${type.name}_selection(x.kind)
    match x.kind:
% for member in type.alternatives:
        case ${type.name}_selection.${member.name}_PRESENT:
            data += encode_${member.type_name}(x.u)
% endfor
    return data

def decode_${type.name}(data : BitStream) -> ${type.name}:
    x = ${type.name}()
    x.kind = decode_${type.name}_selection(data)
    match x.kind:
% for member in type.alternatives:
        case ${type.name}_selection.${member.name}_PRESENT:
            x.u = decode_${member.type_name}(data)
% endfor
    return x

% endif
## OctetStringType
% if isinstance(type, OctetStringType):
%   if isinstance(type.size, RangedSize) and type.size.determinant_name is not None:
def encode_${type.name}(size : int, x : ${type.name}) -> BitArray:
    result = BitArray()
    for item in x:
        result = result + BitArray(uint=item, length=8)
    return result

def decode_${type.name}(size : int, data : BitStream) -> ${type.name}:
    result = []
    for _ in range(0, size):
        item = data[data.bitpos:data.bitpos + 8].uint
        data.bitpos += 8
        result.append(item)
    return result

%   else:
def encode_${type.name}(x : ${type.name}) -> BitArray:
%       if isinstance(type.size, RangedSize):
    result = BitArray(uint=len(x), length=8)
%       else:
    result = BitArray()
%       endif
    for item in x:
        result = result + BitArray(uint=item, length=8)
    return result

def decode_${type.name}(data : BitStream) -> ${type.name}:
%       if isinstance(type.size, RangedSize):
    size = data[data.bitpos:data.bitpos + 8].uint
    data.bitpos += 8
%       else:
    size = ${type.size.size}
%       endif
    result = []
    for _ in range(0, size):
        item = data[data.bitpos:data.bitpos + 8].uint
        data.bitpos += 8
        result.append(item)
    return result

%   endif
% endif
## SequenceOfType
% if isinstance(type, SequenceOfType):
%   if isinstance(type.size, RangedSize) and type.size.determinant_name is not None:
## Using determinant
def encode_${type.name}(size : int, x : ${type.name}) -> BitArray:
    for item in x:
        result = result + encode_${type.element_type_name}(item)
    return result

def decode_${type.name}(size : int, data : BitStream) -> ${type.name}:
    result = []
    for _ in range(0, size):
        item = decode_${type.element_type_name}(data)
        result.append(item)
    return result

%   else:
## Not using determinant
def encode_${type.name}(x : ${type.name}) -> BitArray:
%     if isinstance(type.size, RangedSize):
    result = BitArray(int=len(x), length=8) 
%       else:
    result = BitArray()
%       endif
    for item in x:
        result = result + encode_${type.element_type_name}(item)
    return result

def decode_${type.name}(data : BitStream) -> ${type.name}:
%       if isinstance(type.size, RangedSize):
    size = data[data.bitpos:data.bitpos + 8].int
    data.bitpos += 8
%       else:
    size = ${type.size.size}
%       endif
    result = []
    for _ in range(0, size):
        item = decode_${type.element_type_name}(data)
        result.append(item)
    return result
%   endif

% endif
% endfor
