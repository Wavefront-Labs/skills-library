---
id: computing-software.software-engineering.prolog.phrase-from-file
name: phrase-from-file
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-parsing, phrase-from-file, pure-input, lazy-list, pio]
level: advanced
status: docs-checked
description: "Parse large inputs with phrase_from_file/2,3 and phrase_from_stream/2,3 (library(pure_input)): lazy lists, memory use, the as(chars) option and syntax_error//1."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/pure_input.pl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing files with a DCG (pure input)

`library(pure_input)` is part of pio: it processes input streams with pure predicates, notably DCG rules, which makes non-deterministic processing of input simpler.

```prolog
:- use_module(library(pio)).
:- use_module(library(dcg/basics)).

file_contains(File, Pattern) :-
    phrase_from_file(match(Pattern), File).
match(Pattern) --> string(_), string(Pattern), remainder(_).

?- aggregate_all(count, file_contains('data.txt', `file`), Count).   % pattern must be a code list
```
(This is the module's own documented example: count occurrences of a string in a file. `string//1` and `remainder//1` come from library(dcg/basics).)

## How it works
- `phrase_from_file(:Grammar, +File)` and `/3` with `+Options` are nondet. Options go to `open/4` and `phrase_from_stream/3`.
- The input becomes a lazy list: a partial list ending in an attributed variable. Unifying that tail reads the next block of data (block reads via `read_pending_codes/3`), and the block is stored with the attribute so it is not re-read on backtracking.
- Space use depends on the length of the not-yet-committed part of the grammar. Committed parts of the list are reclaimed by garbage collection. So a grammar that commits (for example with `!`) keeps memory flat; one that keeps choice points over the whole file keeps the list alive.
- `phrase_from_stream(:Grammar, +Stream[, +Options])` runs a grammar on an already open stream. The stream must be buffered; an unbuffered stream raises `permission_error(create, lazy_list, Stream)`.
- Option `as(Type)`: `codes` (default) or `chars`, to run a DCG compiled for character lists rather than codes. `stream_to_lazy_codes/2`, `stream_to_lazy_chars/2` build the lazy list directly (`stream_to_lazy_list/2` is a deprecated alias for codes). The lazy list needs a stream buffer of at least 6 bytes (longest multi-byte sequence) but not a repositionable stream.
- Errors: `syntax_error(+Error)//` throws `error(syntax_error(Error), Location)` at the current input location. `lazy_list_location//1` gives `file(Name, Line, LinePos, CharNo)` or `stream(Stream, Line, LinePos, CharNo)`, or `end_of_file-CharCount` once the list is fully read; `lazy_list_character_count//1` gives only the character count.

## Gotchas
- Pass encoding and similar settings as `open/4` options through `phrase_from_file/3` (options are forwarded to `open/4`).
- The module lists support for other readers (terms, tokens) as a to-do: only character codes or chars are supported.

## Self-check
Count the lines of a large file with a deterministic grammar and observe that memory does not grow with file size, then repeat with a grammar that leaves choice points.

## Checked

Method: 2026-11-08 read all of library/pure_input.pl from the SWI-Prolog repository (exports, pldoc, implementation). Removed claims the file does not state: `term_to_atom`/`read_term_from_atom` coverage, `eos//0` guidance, the CSV memory comparison as fact, and the specific `[encoding(utf8)]` example. The manual landing page and metalevel.at sources were dropped as unread. Documentation only; no commands were run.
