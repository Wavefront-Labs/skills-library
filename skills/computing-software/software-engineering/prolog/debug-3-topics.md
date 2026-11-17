---
id: computing-software.software-engineering.prolog.debug-3-topics
name: debug-3-topics
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, debug-3-topics, prolog-stack]
level: practitioner
status: docs-checked
description: "Print topic-controlled debug messages with debug/3 and catch errors with backtraces using library(debug)."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/debug.pl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# debug/3 topics
```prolog
:- use_module(library(debug)).
work(X) :- debug(work, "processing ~w", [X]).
?- debug(work).          % enable topic
?- nodebug(work).
```
```bash
swipl -s file.pl -g "debug(work)"
```
- `debug(+Topic, +Format, +Args)` formats like `format/3` and writes to `user_error`, prefixed with `% `, only when Topic was enabled with `debug/1`.
- Calls to `debug/3` and `assertion/1` are removed when code is compiled for optimisation, unless the flag `optimise_debug` is `true`.
- `catch_with_backtrace(:Goal, +Catcher, :Recover)` is like `catch/3` but adds a backtrace to the context of `error(Format, Context)` if library(prolog_stack) is loaded.
## Gotchas
- A topic must be enabled before the first message appears; a misspelt topic is silent.
## Self-check
Run the command above and check that `% processing ...` appears on stderr.

## Checked

2026-11-03. SWI-Prolog library(debug) documentation and source (debug.pl): debug/3 semantics, output stream and prefix, optimise_debug, catch_with_backtrace/3; command line `-s`, `-g` from the cmdline page. Removed: the claim that the toplevel loads prolog_stack on demand and the argument-evaluation cost remark (not covered).

Method: documentation only; no commands were run.
