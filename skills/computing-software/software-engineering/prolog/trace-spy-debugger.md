---
id: computing-software.software-engineering.prolog.trace-spy-debugger
name: trace-spy-debugger
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-debugging, trace-spy-debugger, four-port-model]
level: practitioner
status: docs-checked
description: "Debug SWI-Prolog programs with trace/0, spy/1, leash/1, visible/1 and the debugger commands."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/textdebugger.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text debugger
```prolog
?- trace, foo(X).         % trace/0, notrace/0, tracing/0
?- spy(foo/2).            % nospy/1, nospyall/0, debugging/0
?- debug.                 % debug mode: stop only at spy points; nodebug/0 leaves it
?- leash(-all), visible(+all).
?- gtrace.                % graphical tracer (needs XPCE)
```
- Ports: `call`, `redo`, `exit`, `fail`, plus `unify` and `exception`.
- Commands when the debugger pauses: Enter, `c` or space creep; `s` skip; `l` leap to the next spy point; `f` fail; `r` retry; `a` abort; `b` break; `e` exit; `i` ignore; `n` no debug; `u` up; `+` / `-` set / remove spy point; `/` find; `?` or `h` help.
- `leash/1` selects ports where the debugger stops; `visible/1` selects ports that are printed.
- Debug mode disables last-call optimisation.
## Gotchas
- Deep recursion in debug mode uses more stack because last-call optimisation is off.
## Self-check
`spy(foo/2)`, run a goal calling `foo/2`, press `l` to leap and `a` to abort.

## Checked

2026-11-03. SWI-Prolog manual text debugger section (textdebugger.md and builtin.plx in swipl-devel/man): ports, predicate list, command keys, leash/visible, gtrace, debug mode and last-call optimisation. Removed: claims that spy needs the predicate defined and that system predicates are hidden, and `trace/2` as a noise reducer (trace/1,2 set trace points, which is a different purpose).

Method: documentation only; no commands were run.
