---
id: computing-software.software-engineering.ocaml.regular-expressions-str-re-scanf
name: regular-expressions-str-re-scanf
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, regex-scanf, str-library, re-library, scanf, regex]
level: practitioner
status: docs-checked
description: "Match text with Str or Scanf format scanning, with their syntax differences and failure modes."
sources: ["https://ocaml.org/manual/api/", "https://dev.realworldocaml.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regex and Scanf

```ocaml
(* Str *)
let r = Str.regexp "\\([0-9]+\\)-\\([0-9]+\\)"
let () = if Str.string_match r "10-20" 0 then print_string (Str.matched_group 1 "10-20")
let n = Scanf.sscanf "5 abc" " %d %s" (fun n s -> (n, s))
```

## Notes
- `Str` has its own regex syntax with groups written `\\( ... \\)`; `Str.matched_group n s` returns the text of group n of the last match.
- `Scanf` raises `Scanf.Scan_failure`, `Failure` or `End_of_file`; space in the format skips whitespace; `%s` stops at whitespace.
- For complex grammars use a lexer and parser generator such as ocamllex rather than regex.

## Self-check
- [ ] The regex works on both matching and non-matching inputs in a test.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the Str and Scanf API pages (regexp, string_match, matched_group, Scan_failure, format-string whitespace and %s behaviour) and the manual's lexer/parser generator chapter.

Removed or corrected: all Re (ocaml-re) content, the Str thread-safety claim, Angstrom and Menhir recommendations, and the ReDoS claims.

Method: documentation only; no commands were run.
