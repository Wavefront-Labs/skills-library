---
id: computing-software.software-engineering.ocaml.parser-combinators-with-angstrom
name: parser-combinators-with-angstrom
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, angstrom-sedlex, angstrom, parser-combinators, sedlex, unicode-lexer]
level: advanced
status: docs-checked
description: "Parse binary and text formats with Angstrom combinators: backtracking by default, incremental input, commit, fix, chainl1 helper."
sources: ["https://github.com/inhabitedtype/angstrom", "https://raw.githubusercontent.com/inhabitedtype/angstrom/master/lib/angstrom.mli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Angstrom

```ocaml
(* libraries: angstrom *)
open Angstrom
let int = take_while1 (function '0'..'9' -> true | _ -> false) >>| int_of_string
let sum = sep_by1 (char '+') int >>| List.fold_left ( + ) 0
let r = parse_string ~consume:All sum "1+2+3"      (* Ok 6 *)
```

## Notes
- Angstrom is a parser-combinator library with monadic and applicative interfaces. It supports incremental input through buffered and unbuffered (zero-copy) interfaces, and works with Async and Lwt.
- Parsers backtrack by default and support unbounded lookahead (unlike Parsec-style libraries that need `try`). `commit` prevents backtracking beyond the current position so the input buffer can reuse earlier bytes.
- `fix` builds parsers for inductive types (trees, sequences, expressions).
- Angstrom does NOT include infix combinators such as `chainl1`; the README defines it in a few lines using `lift2`, `>>=` and `<|>`, then builds an arithmetic parser from it.
- `p <?> name` associates a name with a parser, reported on failure. The README table lists "reports line numbers in errors" as not supported.
- `parse_string ~consume:All` requires the parser to reach end of input; `~consume:Prefix` lets it succeed without reaching eof.
- The source distribution has HTTP (RFC 2616) and JSON (RFC 7159) example parsers.

## Self-check
- [ ] The expression 1+2+3 parses to Ok 6 in a test.

## Checked

2026-11-08. Read in full: Angstrom README and lib/angstrom.mli entries for take_while1, sep_by1, fix, <?>, commit, parse_string.
Removed: the sedlex section and Menhir advice (no cited source), the claim that a failed branch does not rewind, and the claim that chainl1 ships with the library (it does not).
Method: documentation only; no commands were run.
