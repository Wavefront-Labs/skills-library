---
id: computing-software.software-engineering.scheme-racket.xrepl
name: xrepl
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, xrepl]
level: practitioner
status: docs-checked
description: "Use XREPL comma commands in the racket REPL: ,help, ,enter, ,require, ,time, ,backtrace, ,syntax and past results ^ ^^."
sources:
  - https://docs.racket-lang.org/xrepl/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XREPL (eXtended REPL)
**Goal:** productive REPL.
```text
$ racket
> ,help
> ,enter "main.rkt"
> ,time (sleep 0.1)
> ,top
```
- XREPL is enabled by default when `racket` starts a REPL and the xrepl module is available (loaded via `racket/interactive`); since xrepl-lib 6.7 no install is needed. `,install!` is kept for init-file setup.
- Meta commands are typed at the REPL prefixed by a comma. `,help [name]` lists commands (synonyms `,h ,?`).
- `,enter [module]` goes inside a module's namespace (reloading it if already inside); `,toplevel` / `,top` or `,enter #f` returns. `,require` (`,req`, `,r`) accepts file names as symbols; `,require-reloadable` (`,rr`) makes a module reloadable by turning off `compile-enforce-module-constants`.
- Debugging: `,backtrace` (`,bt`) shows the context of the last error (not printed automatically); `,exn` shows the exception; `,time [count] expr` times an expression (with a count it repeats and averages); `,trace` / `,untrace`; `,profile expr` runs the statistical profiler; `,errortrace` toggles instrumentation and must be set before loading the code.
- `,syntax expr` with flags `+` (expand-once), `!` (expand), `*` and `**` (macro-debugger textual steps).
- `,edit` runs the editor named by the EDITOR environment variable; if unset, use `,drracket`. `,cd`, `,pwd`, `,shell` exist.
- Past results: `^` is the last printed result, `^^` the one before, up to five; `$1` .. `$5` are aliases. `#<void>` results are not kept, and values are weakly held.
## Self-check
`,time (sleep 0.1)` reports timings; `(list ^ ^^)` after two results shows them in reverse order.

## Checked
2026-11-08. Confirmed against the XREPL manual page: default enablement, 6.7 change note, command names and synonyms, ,enter / ,top behaviour, ,time count semantics, ,backtrace behaviour, ,syntax flags, ,edit and EDITOR, past-result variables. Removed: the `racket -il xrepl` invocation (the manual says XREPL is on by default and does not document that flag) and the raco source (unrelated).
Method: documentation only; no commands were run.
