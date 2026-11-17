---
id: computing-software.software-engineering.ocaml.lexers-and-parsers-with-ocamllex-menhir
name: lexers-and-parsers-with-ocamllex-menhir
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, ocamllex-menhir, ocaml-parsing, ocamllex, menhir, parser-generator, dune-menhir]
level: advanced
status: docs-checked
description: "Write a lexer in ocamllex and a grammar in Menhir, wire them in dune with ocamllex and menhir stanzas, and use Menhir error tooling."
sources: ["https://gallium.inria.fr/~fpottier/menhir/manual.html", "https://raw.githubusercontent.com/ocaml/dune/main/doc/reference/dune/menhir.rst", "https://raw.githubusercontent.com/ocaml/dune/main/doc/reference/dune/ocamllex.rst", "https://ocaml.org/manual/5.5/lexyacc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ocamllex + Menhir

```lisp
(ocamllex lexer)
(menhir (modules parser))
(library (name calc))
```
```
(* lexer.mll *)
{ open Parser }
rule token = parse
  | [' ' '\t' '\n'] { token lexbuf }
  | ['0'-'9']+ as n { INT (int_of_string n) }
  | '+' { PLUS } | eof { EOF }
(* parser.mly *)
%token <int> INT
%token PLUS EOF
%start <int> main
%%
main: e = expr EOF { e }
expr: a = expr PLUS b = INT { a + b } | n = INT { n }
```
```ocaml
let parse s = Parser.main Lexer.token (Lexing.from_string s)
```

## Notes
- `(ocamllex <names>)` is shorthand for a rule that runs `ocamllex -q -o <name>.ml` on `<name>.mll`. The long form `(ocamllex (modules ...) (mode ...))` selects a rule mode.
- A `(menhir (modules <parser> ...))` stanza needs `(using menhir <version>)` in `dune-project`; if absent, Dune adds the line with the latest Menhir version when it sees a menhir stanza. Optional fields: `merge_into` (same as `--base`), `flags`, `infer`.
- From Menhir stanza version 3.0, Dune generates a `.conflicts` file by default; control it with `(explain <blang expression>)`.
- Menhir CLI: `--explain` writes conflict explanations; `--list-errors` produces a `.messages` file listing error states; `.messages` files can be merged, compared and compiled for custom syntax-error messages. Precedence declarations are `%left`, `%right`, `%nonassoc` and `%prec`.
- Menhir has monolithic, incremental and inspection APIs; the incremental API needs `MenhirLib`.
- `Lexing.from_string` and `Lexing.from_function` create lexer buffers; `eof` is a pattern in ocamllex rules.

## Self-check
- [ ] Parsing "1+2+3" returns 6.

## Checked
Date: 2026-11-08. Confirmed against the Dune menhir and ocamllex reference pages (read in full) and the OCaml 5.5 manual lexyacc page (searched for Lexing.from_string and eof only). The Menhir manual page was searched for the flags and API names above, not read in full. Removed: the `(using menhir 2.1)` version, the `Lexing.new_line` and `lex_curr_p` advice, the `Parser.Error` claim, the sedlex note and the gallium landing and ocaml.org/docs sources.
Method: documentation only; no commands were run.
