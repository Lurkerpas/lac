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

<html>
<head>
<style>
table, th, tr, td {
  border: 1px solid black;
  border-collapse: collapse;
}
.header {
    background-color: #a0a0a0
}
</style>
<title>
Module ${module_name}
</title>
</head>

## Type declarations
% for type in module.types.values():
## SequenceType
% if isinstance(type, SequenceType):
<p>
<strong>${type.name}</strong>
<table>
<tr class="header">
% for member in type.elements:
<th>${member.name}</th>
% endfor
</tr>
<tr>
% for member in type.elements:
<th>${member.type_name}</th>
% endfor
</tr>
</table>
</p>
% endif
% endfor

</html>