---
id: computing-software.cybersecurity-defensive.falco.transformers-and-val
name: transformers-and-val
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [transformers, tolower, basename, val, field-comparison]
level: practitioner
status: docs-checked
description: "Apply tolower, toupper, b64, basename and len to Falco fields, and compare two fields with val()."
sources:
  - https://falco.org/docs/concepts/rules/conditions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Falco supports basic transformations on fields inside rule conditions. Example for a case-insensitive process name: `tolower(proc.name) = bash`.

Supported transformers:
- `tolower(<field>)` and `toupper(<field>)`.
- `b64(<field>)`: decodes the field from Base64.
- `basename(<field>)`: the filename without its directory. Unlike the Unix program, it returns `""` when no filename is present. `basename(proc.exepath)` is `"cat"` for `/usr/bin/cat` but `""` for `/usr/bin/`.
- `len(<field>)`: number of elements for LIST fields, characters for CHARBUF fields, bytes for BYTEBUF fields.

Comparing fields: normally the right-hand side is a constant. To compare against another field, wrap it in the special `val()` transformer. To find processes whose name equals their parent name:
`proc.name = val(proc.pname)`.
Transformers may appear on both sides:
`tolower(proc.name) = tolower(proc.pname)`.

Gotcha: `val()` is documented for the right-hand side of a comparison, so use `proc.name = val(proc.pname)` for field-to-field tests; a bare field name on the right is not documented as a field reference.

## Checked

2026-11-08. Read the Condition Syntax page in full. Removed an unsupported output-transformer example and an unsupported val() gotcha.

Method: documentation only; no commands were run.
