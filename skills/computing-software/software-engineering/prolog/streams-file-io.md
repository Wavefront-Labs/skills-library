---
id: computing-software.software-engineering.prolog.streams-file-io
name: streams-file-io
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, streams-file-io, readutil, swi-prolog, file-io]
level: practitioner
status: docs-checked
description: "Read lines, whole files and terms with library(readutil): read_line_to_string/2, read_file_to_string/3, read_file_to_codes/3, read_file_to_terms/3, and EOF behaviour."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/readutil.pl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading streams and files with library(readutil)

```prolog
:- use_module(library(readutil)).
lines(File, Ls) :- read_file_to_string(File, S, []), split_string(S, "\n", "", Ls).
?- read_file_to_terms('facts.pl', Terms, []).
?- open(F, read, S, [encoding(utf8)]), read_line_to_string(S, L), close(S).
```

## Predicates (exports and pldoc)
| Predicate | Behaviour |
|---|---|
| `read_line_to_string(+Stream, -String)` | next line without terminator; unifies with the atom `end_of_file` at end of file (not a string) |
| `read_line_to_codes(+Stream, -Codes)` | line as codes without the newline; `end_of_file` at EOF in the Prolog fallback |
| `read_line_to_codes(+Stream, -Codes, ?Tail)` | difference-list version that keeps the newline; useful to read a block of lines up to a delimiter (the pldoc example reads an HTTP header ended by a blank line) |
| `read_stream_to_codes(+Stream, -Codes)` and `/3` | whole remaining input as codes; `/3` gives a difference list |
| `read_file_to_codes(+Spec, -Codes, +Options)` | whole file as codes; option `tail(Tail)` makes `Codes\Tail` a difference list |
| `read_file_to_string(+Spec, -String, +Options)` | whole file as a string |
| `read_file_to_terms(+Spec, -Terms, +Options)` | all terms in the file; `tail(Tail)` supported |

- `Spec` is resolved with `absolute_file_name/3` with `access(read)`. `Options` is a list that is split over `absolute_file_name/3`, `open/4` (so `encoding(utf8)` and similar open options work) and, for terms, `read_term/3`. A non-list `Options` raises a type error.
- Files are opened and closed with `setup_call_cleanup/3` inside these predicates; use the same pattern for streams you open yourself.
- `read_file_to_terms/3`: output options of `read_term/3` such as `variable_names` or `subterm_positions` make the call fail on files with several terms, because the values for different terms do not unify.
- The line and stream readers are implemented in C for speed, linked at runtime, with a Prolog fallback if the shared object is missing.
- Related: `phrase_from_file/3` (library(pure_input)) to process a file with a DCG, and library(lazy_lists).

## Self-check
Read a file line by line with `read_line_to_string/2` until `end_of_file` and compare the count with a line count from another tool.

## Checked

Method: 2026-11-08 read all of library/readutil.pl from the SWI-Prolog repository (exports, pldoc, fallback implementation). Removed claims not found there: standard stream aliases, `exists_file`/`directory_files`/`copy_stream_data` usage, and the "default encoding follows the locale" note. The manual landing page and metalevel.at sources were dropped as unread. Documentation only; no commands were run.
