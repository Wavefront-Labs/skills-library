---
id: computing-software.software-engineering.ocaml.compiler-warnings-and-linting
name: compiler-warnings-and-linting
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, warnings-linting, warnings-flags, ocaml-warnings, unused-variable, strict-sequence]
level: practitioner
status: docs-checked
description: "Control warnings with -w, -warn-error and [@@@warning], and the warnings worth keeping as errors."
sources: ["https://ocaml.org/manual/native.html", "https://ocaml.org/manual/attributes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Warnings

```bash
ocamlopt -w +a-4-9-40-41-42-44-45-70 -warn-error +a-3 -strict-sequence x.ml
ocamlopt -warn-help      # list all warnings of your compiler
```
```ocaml
[@@@warning "-32"]            (* disable unused value for this file *)
let _x = 1 [@@warning "-32"]
```

## Notes
- Spec: `+n` enable, `-n` disable, `@n` enable and make fatal; ranges `n1..n2`; letters select sets of warnings. `-warn-error` marks which warnings are fatal.
- Prefer disabling a warning locally with `[@@@warning "-n"]` or `[@@warning "-n"]` over disabling it globally.
- Most valuable: 8 (non-exhaustive), 9 (missing record fields), 11/12 (redundant case), 26/27 (unused variable), 32-39 (unused definitions), 6 (labels omitted), 4 (fragile match), 44/45 (open shadowing).
- `-strict-sequence` makes `e1; e2` require `e1 : unit`.
- `_unused` prefix silences unused variable warnings.

## Self-check
- [ ] CI compiles with the same `-w` and `-warn-error` settings used locally.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the ocamlopt page (-w and -warn-error syntax, ranges, letters, -strict-sequence, -warn-help, the warning numbers and names 4, 6, 8, 9, 11, 12, 26, 27, 32-39, 40, 41, 42, 44, 45, 70) and the attributes chapter ([@@@warning], [@@warning]).

Removed or corrected: dune profile claims, the -alert option, the opt-in remark for warning 4, and the odoc source link.

Method: documentation only; no commands were run.
