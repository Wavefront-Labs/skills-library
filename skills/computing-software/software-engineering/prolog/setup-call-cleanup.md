---
id: computing-software.software-engineering.prolog.setup-call-cleanup
name: setup-call-cleanup
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, setup-call-cleanup, assertion-1]
level: advanced
status: docs-checked
description: "Guarantee resource release with setup_call_cleanup/3 and check invariants with assertion/1 in SWI-Prolog."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/builtin.plx
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/debug.pl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cleanup and assertions
```prolog
read_first(File, Line) :-
    setup_call_cleanup(open(File, read, S),
                       read_line_to_string(S, Line),
                       close(S)).
:- use_module(library(debug)).
f(X) :- assertion(integer(X)), true.
```
`setup_call_cleanup(Setup, Goal, Cleanup)` calls `once(Setup)` then `Goal`. If Setup succeeds, Cleanup runs exactly once when Goal finishes: on failure, deterministic success, commit (cut) or exception. Setup is protected from asynchronous interrupts such as `call_with_time_limit/2`.
## Gotchas
- If Goal leaves a choice point, Cleanup waits until it is cut or exhausted; wrap Goal in `once/1` to release early.
- Success or failure of Cleanup is ignored and its choice points are destroyed.
- `assertion(Goal)` has no effect when Goal succeeds. On failure or exception it calls `prolog:assertion_failed/2`; if that fails, an interactive toplevel thread prints a message and the stack trace and traps the debugger, any other thread throws `error(assertion_error(Reason, Goal), _)`.
- Calls to `assertion/1` and `debug/3` are removed when code is compiled for optimisation unless the flag `optimise_debug` is `true`. Use `must_be/2` for argument validation that must survive.
## Self-check
Open a non-existent file with `setup_call_cleanup`: Setup raises, so Cleanup (`close/1`) must not run.

## Checked

2026-11-03. SWI-Prolog manual setup_call_cleanup/3 section (once(Setup), cleanup conditions, interrupt protection, Cleanup result ignored) and library(debug) source documentation for assertion/1 (assertion_failed hook, interactive versus other threads) and optimise_debug. Removed: "failure throws `assertion_failed`" (the documented behaviour is the thread-dependent one above); the read_line_to_string/1 and must_be/2 calls are used as in the source skill and are not covered by the pages read, so they are only examples.

Method: documentation only; no commands were run.
