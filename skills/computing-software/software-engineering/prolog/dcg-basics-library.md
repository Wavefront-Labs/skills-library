---
id: computing-software.software-engineering.prolog.dcg-basics-library
name: dcg-basics-library
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, dcg-basics-library, dcg-basics, swi-prolog, parsing]
level: practitioner
status: docs-checked
description: "Reuse library(dcg/basics) nonterminals (integer//1, number//1, blanks//0, string//1, string_without//2, eos//0) and know which are lazy or leave choice points."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/dcg/basics.pl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# library(dcg/basics)

Primitives on lists of character codes; classification uses `code_type/2`.

```prolog
:- use_module(library(dcg/basics)).
kv(K-V) --> string_without(`=`, Kc), "=", integer(V), { atom_codes(K, Kc) }.
?- phrase(kv(P), `age=42`).           % P = age-42
?- phrase((blanks, number(N), blanks), `  3.14 `).
```

## Exported nonterminals (module header and pldoc)
| Nonterminal | Meaning |
|---|---|
| `white//0`, `whites//0` | one or zero-or-more white characters, not newline (`whites` is det) |
| `blank//0`, `blanks//0` | space characters including newline; `blanks` is det |
| `blanks_to_nl//0` | blanks followed by a newline or end of input |
| `nonblank//1`, `nonblanks//1` | `graph` characters |
| `string//1` | as few codes as possible, one more on each backtrack (nondet); normally followed by a delimiter test |
| `string_without//2` | as many codes as possible until one in `EndCodes` (a code list or a string); the terminator stays in the input |
| `digit//1`, `digits//1` | one digit, or a possibly empty run |
| `integer//1` | optional sign then a non-empty digit sequence |
| `float//1`, `number//1` | floats and integers; conversion via `number_codes/2`; `number//1` and `integer//1` can also generate when bound |
| `xdigit//1`, `xdigits//1`, `xinteger//1` | hexadecimal weights (0-15) and values; sign allowed on `xinteger` |
| `alpha_to_lower//1` | read a letter, return it lower-case |
| `eol//0` | `\n`, `\r\n`, or end of input |
| `eos//0` | end of input |
| `remainder//1` | unify with the rest of the input |
| `csym//1`, `prolog_var_name//1` | C identifier; Prolog variable name |
| `atom//1` | generate the codes of a ground atom |

## Gotchas
- `string//1` is the lazy one: use it as `string(Codes), ":", !, ...` so the delimiter test ends the search (the pldoc example cuts after the delimiter).
- `string_without//2` is greedy and deterministic; prefer it when the terminating set is known.
- `eos//0` is documented as violating the context-free property of DCGs; the library note says the exact problems are still to be explained.
- The library calls itself a starting point; check the exports before assuming a nonterminal exists.

## Self-check
Parse `x=12` into `x-12` using only library(dcg/basics) with `phrase/2` (end the rule with `eos`).

## Checked

Method: 2026-11-08 read the full library/dcg/basics.pl source from the SWI-Prolog repository (exports, pldoc comments and clause bodies). Removed claims not found there: the pushback rule note (`a, [x] --> b`) and the `double_quotes` flag remarks. The manual landing page and metalevel.at source were dropped as unread. Documentation only; no commands were run.
