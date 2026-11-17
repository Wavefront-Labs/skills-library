---
id: computing-software.software-engineering.prolog.read-write-terms
name: read-write-terms
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-io, read-write-terms, writeq-print]
level: practitioner
status: docs-checked
description: "Read and write Prolog terms with read_term/2, write_term/2, print/1, writeq/1 and write_canonical/1 and their default options."
sources:
  - https://www.swi-prolog.org/pldoc/man?predicate=write_term/2
  - https://www.swi-prolog.org/pldoc/man?predicate=write_canonical/1
  - https://www.swi-prolog.org/pldoc/man?predicate=read_term/2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading and writing terms
```prolog
?- writeq('Hello World').          % 'Hello World' (quoted, so it reads back)
?- write_canonical([a,'B'|T]).     % [a,'B'|_]  (singleton variables print as _)
?- print(foo('X')).                % portray(true), numbervars(true), quoted(true)
?- read_term(user_input, T, [variable_names(Vs)]).
?- write_term(f(X,'a b'), [quoted(true), max_depth(3)]).
?- with_output_to(string(S), print([1,2])).
```
- Default options: `write/1` is `[numbervars(true)]`, `writeq/1` is `[numbervars(true), quoted(true)]`, `print/1` follows the flag `print_write_options`, `write_canonical/1` is quoted, ignores operators and names other variables `A`, `B`, ...
- `write_term/2` options include `quoted(Bool)`, `max_depth(Integer)` (0 = no limit), `cycles(Bool)`, `numbervars(Bool)`, `variable_names(List)`.
- `read_term/2,3` unifies the term with `end_of_file` at end of input; `term_string/2` and `term_to_atom/2` read a term from text.
## Gotchas
- `write/1` drops quotes, so the output may not read back; use `writeq/1` or `write_canonical/1` for round trips.
- The toplevel prints answers with `answer_write_options`, default `[quoted(true), portray(true), max_depth(10), attributes(portray)]`, so long lists end in `...`.
- Use `format/1-3` for text; `portray_clause/1` pretty-prints clauses.
## Self-check
Round-trip `f('A b', "str", X)` through `with_output_to(string(S), writeq(...))` and `term_string/2`.

## Checked

2026-11-03. SWI-Prolog manual section "Term reading and writing": default option table for print/write/write_canonical/writeln/writeq, write_term/2 options (max_depth example, cycles, quoted, variable_names), read_term end_of_file and term_string/2 mention, flag answer_write_options (overview.plx), format/3 sinks via with_output_to/2. Removed: the wrong `[a,'B'|A]` output for write_canonical (a single-occurrence variable prints `_`), "print uses portray_clause style quoting", and the unverified "read/1 expects a terminating dot".

Method: documentation only; no commands were run.
