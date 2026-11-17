---
id: computing-software.software-engineering.ocaml.json-with-yojson-and-ppx
name: json-with-yojson-and-ppx
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, json-yojson, ocaml-serialization-cli, yojson, ppx-deriving-yojson, json-parsing]
level: practitioner
status: docs-checked
description: "Parse JSON with Yojson.Safe and choose among ppx_deriving_yojson, ppx_yojson_conv, atd and jsonm for typed or streaming JSON."
sources:
  - https://raw.githubusercontent.com/ocaml-community/yojson/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Yojson

Yojson parses JSON and JSON5 data into nested OCaml tree data structures (the `yojson` and `yojson-five` libraries; docs for both are on ocaml.org).

```ocaml
(* dune: (libraries yojson) *)
let json_string = {|
  {"number" : 42,
   "string" : "yes",
   "list": ["for", "sure", 42]}|}

let json = Yojson.Safe.from_string json_string   (* : Yojson.Safe.t *)

let () = Format.printf "Parsed to %a" Yojson.Safe.pp json
```

## Choosing tooling built on Yojson
- `ppx_deriving_yojson`: generates code converting between `Yojson.Safe.t` and your own OCaml types.
- `ppx_yojson_conv` (Jane Street): an alternative to the above with different design decisions.
- `atd`: generates mapping code from `.atd` specification files, usable from several languages.
- `jsonm`: an alternate parser producing a stream of items, so the whole structure need not be in memory.
- The README's `examples` directory has more examples. It does not cover error handling, the `Util` accessors, the ppx attributes or the `Basic` module; look those up in the ocaml.org API docs and each ppx's own README.

## Self-check
- [ ] Parsing the string above and printing it with `Yojson.Safe.pp` shows the same three fields.

## Checked

2026-11-08. Read: the yojson README in full.
Removed: `Util` accessors, `to_string` of polymorphic variants, exception names (`Json_error`, `Type_error`), `Basic` versus `Safe` differences, `Intlit` handling, ppx attributes (`[@key]`, `[@default]`, `[@opaque]`), `t_of_yojson` naming, the stack-depth warning, and the ocaml.org/docs and cmdliner sources (not about JSON, not read).
Method: documentation only; no commands were run.
