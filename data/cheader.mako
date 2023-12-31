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
    OctetStringType, \
    FixedSize, \
    RangedSize
%>
## Python definitions
<%
module_name = module.name.upper()
%>
## Standard C type includes
#ifndef ${module_name}_H
#define ${module_name}_H

#include <stdint.h>
#include <stdbool.h>

## Includes for imported types
% for include in module.imports:
#include "${include.module_name}.h"
% endfor

## Debug list of types
% for type in module.types.values():
// ${type.name}
% endfor

## Type declarations
% for type in module.types.values():
## IntegerType
% if isinstance(type, IntegerType):
<% 
    size = type.encoding.options.size.size
    if type.range.min > 0:
        if size <= 8:
            c_type_name = "uint8_t"
        elif size <= 16:
            c_type_name = "uint16_t"
        elif size <= 32:
            c_type_name = "uint32_t"
    else:
        if size <= 8:
            c_type_name = "int8_t"
        elif size <= 16:
            c_type_name = "int16_t"
        elif size <= 32:
            c_type_name = "int32_t"
%>\
typedef ${c_type_name} ${type.name};

% endif
## RealType
% if isinstance(type, RealType):
typedef float ${type.name};

% endif
## BooleanType
% if isinstance(type, BooleanType):
typedef bool ${type.name};

% endif
## EnumerationType
% if isinstance(type, EnumerationType):
typedef enum
{
% for value in type.values:
%   if value.value is not None:
    ${value.name} = ${value.value},
%   else:
    ${value.name},
%   endif
% endfor
} ${type.name};

% endif
## SequenceType
% if isinstance(type, SequenceType):
typedef struct
{
% for member in type.elements:
% if not member.acn:
    ${member.type_name} ${member.name};
% endif
% endfor
} ${type.name};

% endif
## ChoiceType
% if isinstance(type, ChoiceType):
typedef enum {
<% count = 0 %>\
% for member in type.alternatives:
    ${member.name}_PRESENT = ${count}, <% count = count + 1 %>
% endfor
} ${type.name}_selection;

typedef union {
% for member in type.alternatives:
    ${member.type_name} ${member.name};
% endfor
} ${type.name}_unchecked_union;

typedef struct {
    ${type.name}_selection kind;
    ${type.name}_unchecked_union u;
} ${type.name};

% endif
## OctetStringType
% if isinstance(type, OctetStringType):
%   if isinstance(type.size, RangedSize):
typedef struct
{
    int nCount;
    uint8_t arr[${type.size.range.max}];
} ${type.name};
%   else:
typedef struct
{
    uint8_t arr[${type.size.size}];
} ${type.name};
%   endif

% endif
## SequenceOfType
% if isinstance(type, SequenceOfType):
%   if isinstance(type.size, RangedSize):
typedef struct
{
    int nCount;
    ${type.element_type_name} arr[${type.size.range.max}];
} ${type.name};
%   else:
typedef struct
{
    ${type.element_type_name} arr[${type.size.size}];
} ${type.name};
%   endif

% endif
% endfor
#endif // ${module_name}_H