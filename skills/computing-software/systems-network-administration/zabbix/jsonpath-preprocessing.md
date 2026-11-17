---
id: computing-software.systems-network-administration.zabbix.jsonpath-preprocessing
name: jsonpath-preprocessing
category: computing-software
field: systems-network-administration
product: zabbix
tags: [jsonpath, json-path, preprocessing, filter-expression, json, extract]
level: practitioner
status: docs-checked
description: "Extract values from JSON with the JSONPath syntax Zabbix supports, including filters, functions and detached segments."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/preprocessing/jsonpath_functionality
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
JSONPath in Zabbix is dot- or bracket-separated segments starting at $. These are equivalent: $.object.name, $.object['name'], $["object"]['name'].

Segments: a name, * for all properties, ['a','b'] for several names, [n] for an array index, [n,m] for several indexes, [*] for all, [start:end] for a range (end excluded, negative counts from the end), and [?(expression)] for a filter.

Functions at the end of a path: length() counts array elements, first() takes the first element of an array. Examples:
- $.object.history.length() returns the number of history elements.
- $[?(@.name == 'Object')].price.first() returns price of the first object named Object.
- $[?(@.price > 10)].length() counts objects with price over 10.

Prefix a segment with two dots (..) to match ignoring ancestry: $..name returns every name property. A trailing tilde extracts the matched property name or array index, as a string.

Filter expressions use infix arithmetic with operands such as text constants, numbers, $ paths from the document root and @ paths from the current element. Only definite paths are supported inside filters.

Definite path results are returned as is; indefinite paths return an array. If a macro value from low-level discovery is placed into a JSONPath, special characters must be escaped; see the LLD escaping page.

Indefinite paths (detached, multiple names or indexes, slices, filters) return an array, and a function makes the path definite.

## Checked

2026-11-09. Confirmed against the Zabbix manual page JSONPath functionality (current): path forms, supported segments, range semantics, detached .. segments, tilde suffix, filter operands, the length() and first() functions and their examples, definite versus indefinite output, LLD macro escaping pointer. Removed the Custom on fail advice, which the page does not state.

Method: documentation only; no commands were run.
