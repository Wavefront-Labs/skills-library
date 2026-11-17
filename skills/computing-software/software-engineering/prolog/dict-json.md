---
id: computing-software.software-engineering.prolog.dict-json
name: dict-json
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, dict-json, json-read-dict]
level: practitioner
status: draft
description: "Convert between dicts and JSON with library(http/json): json_read_dict/2, json_write_dict/2, atom_json_dict/3."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dicts and JSON
```prolog
:- use_module(library(http/json)).
?- atom_json_dict('{"a": [1,2], "b": "x"}', D, []).     % D = _{a:[1,2], b:"x"}
?- json_write_dict(current_output, _{k: 1, l: [true]}).
?- open('in.json', read, S), json_read_dict(S, D), close(S).
?- atom_json_term('{"a":1}', T, []).                     % json([a=1]) classic form
```
- Strings parse as Prolog strings with `json_read_dict`, atoms with the older `json_read`.
- `json_write_dict(Out, Dict, [width(0)])` for compact output.
## Gotchas
- `null`, `true`, `false` map to atoms by default; set `null/1` options to change.
- Library path moved to `library(json)` in newer versions (unconfirmed which release).
## Self-check
Round trip a nested dict through JSON text and compare with `==`.
