---
id: computing-software.software-engineering.ocaml.printf-and-format-module
name: printf-and-format-module
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, printf-format, ocaml-text-formatting, printf, format-boxes, pp-function, sprintf]
level: practitioner
status: docs-checked
description: "Use Printf format strings, Format boxes and break hints, and write pp functions with Fmt-style combinators."
sources: ["https://ocaml.org/manual/api/", "https://dev.realworldocaml.org/", "https://github.com/ocaml/ocaml/tree/trunk/stdlib", "https://github.com/ocaml/ocaml/tree/trunk/manual/src"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Printf and Format

```ocaml
Printf.printf "%d %s %.2f %c %b\n" 1 "a" 3.14159 'x' true
let s = Printf.sprintf "%-10s|%5d" "ab" 42
let pp_pair ppf (a, b) = Format.fprintf ppf "@[<hv 1>(%d,@ %d)@]" a b
let () = Format.printf "%a@." pp_pair (1, 2)
let msg = Format.asprintf "%a" pp_pair (1, 2)
```

## Notes
- The format string is type-checked at compile time; it must be a literal (or a `format` value, `("%d" : _ format)`).
- `%a` takes a printer function and a value; `%t` takes a printer only; `%S` quotes like OCaml syntax; `%i` = `%d`; `%x`, `%08.3f`, `%e`, `%g` work like C.
- `Format`: boxes `@[ ... @]`, break hints `@ ` (space or newline), `@,`, `@;<1 2>`; `@.` flushes with newline; `@\n` forces newline.
- Flush stdout: `Printf.printf "..%!"` or `flush stdout`; `Format.printf` needs `@.` or `%!`.
- `Format.kasprintf` builds strings from format args in error constructors.

## Self-check
- [ ] Output of a long list wraps at the Format margin (`Format.set_margin 80`).

## Checked
2026-11-02. Confirmed: Printf/Format specifiers, boxes, break hints, flushing (printf.mli, format.mli). Removed: Fmt library.
Method: documentation only (OCaml stdlib .mli files and manual .etex sources from github.com/ocaml/ocaml, trunk); no commands were run.
