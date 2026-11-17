---
id: computing-software.software-engineering.ocaml.programming-guidelines-and-naming
name: programming-guidelines-and-naming
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, ocaml-style-guidelines, programming-guidelines, naming-conventions, ocaml-style]
level: practitioner
status: docs-checked
description: "Apply the ocaml.org programming guidelines: underscore names, mli docs, qualified access over open, exhaustive matches, narrow exception handlers."
sources:
  - https://ocaml.org/docs/guidelines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Programming guidelines and style

## Conventions (from the ocaml.org guidelines)
- Formatting: OCamlFormat can format code automatically, so review can focus on the non-automated practices below.
- Separate words in identifiers with underscores (`int_of_string`, not `intOfString`). Capitalised words are reserved for constructors and module names, so `IntOfString` cannot be a function name. Exception: keep the library's own capitalisation when interfacing with an existing library that uses it.
- Global names may be long and descriptive, not abbreviated. Local identifiers can be brief and reused from function to function; avoid look-alikes such as `l` or `O`.
- Give the same name to arguments with the same meaning; add numeral suffixes when several share a meaning (`expr1`, `expr2`).
- Split programs into coherent modules, write an explicit interface (`.mli`) for each, and document the functions, types and exceptions it defines. Put a function's usage description in the interface, not the implementation.
- Avoid `open`; use qualified identifiers and short meaningful module names. Accepted exceptions: a module that deliberately redefines a set of functions (the guide's example is `Format`, whose print functions shadow `Stdlib` ones, so opening it avoids silently mixing the two), modules of shared type definitions, and large libraries such as the arbitrary-precision integer one (the guide opens `Num` for `fib`).
- Pattern matching: avoid non-exhaustive matches, and avoid a catch-all `| _ -> ...` when the type is a concrete one defined in your program; list the remaining constructors explicitly so that adding a constructor triggers a compiler warning.
- Treat compiler warnings as errors to fix, especially pattern-matching warnings (remove useless clauses, complete non-exhaustive matches).
- Prefer assertions to comments for argument checks (`assert (x >= 0)`); avoid comments that add no information; comment inside function bodies only where the code is genuinely difficult (for example mutation-heavy code).
- Exceptions: reuse predefined exceptions where they fit (the guide cites `Not_found` for failed searches), handle exceptions a call may raise with `try ... with`, and do not use `try ... with _ ->` outside the program's main function; if you must catch everything to restore an invariant, re-raise afterwards.

## Self-check
- [ ] Every module has an `.mli` that documents its public values.
- [ ] No `| _ ->` catch-all over a concrete variant defined in the project.

## Checked

2026-11-08. Read: the lines of https://ocaml.org/docs/guidelines covering the general guidelines, comments, identifiers, modules, pattern matching, compiler warnings and exceptions sections. Later sections (data structures, imperative style, formatting rules) were not read in full and nothing from them is used.
Removed: the `t`/`create`/`make`/`to_x`/`is_x` conventions, `*_exn`/`*_opt` naming, labelled-argument advice, equal/compare/pp advice, result-over-exceptions advice, `Obj.magic`, test layout and `dune test` claims (none appear in the sections read), and the odoc source (not read).
Method: documentation only; no commands were run.
