---
id: computing-software.software-engineering.prolog.initialization-directive
name: initialization-directive
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, initialization-directive, initialization-main]
level: practitioner
status: docs-checked
description: "Run goals at load time or program start with initialization/1,2, the main option, library(main) and argv_options/3."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/builtin.plx
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/main.pl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# initialization
```prolog
:- initialization(setup).             % after_load: when this file has been loaded
:- initialization(main, main).        % program entry point
:- use_module(library(main)).
main(Argv) :- argv_options(Argv, Pos, Opts), writeln(Pos-Opts).
```
- `initialization(Goal)` is `initialization(Goal, after_load)`. `now` runs Goal immediately; `main` wraps Goal as the program; `program` and `restore_state` / `prepare_state` relate to saved states.
- With `main`, the last registered main goal runs at startup; failure or an exception gives a non-zero exit status, and the toplevel defaults to `halt/0`, so success exits with 0. An explicit `-t` toplevel runs normally.
- `library(main)`: `main/0` installs a SIGINT handler that terminates with status 1 and calls `main/1` with the command-line arguments; `argv_options/3,4` split them into positional arguments and options.
- The flag `argv` holds the arguments left after Prolog processed its own options.
- Scripts can start with `#!` (see the scripting section of the manual).
## Gotchas
- A plain directive `:- go.` runs while loading; `initialization/1` waits until the file is loaded.
## Self-check
Run `swipl script.pl a b` and verify that `main/1` receives `[a,b]` and the exit status is 0.

## Checked

2026-11-03. SWI-Prolog manual: initialization/1,2 (when values, main semantics and exit status), library(main) documentation (main/0, argv_options/3,4), flag argv, scripting section (`#!`). Removed: the Ctrl-C claim attached to initialization/2 itself and the quoted "Goal (directive) failed" warning text (not covered).

Method: documentation only; no commands were run.
