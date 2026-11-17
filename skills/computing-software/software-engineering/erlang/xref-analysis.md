---
id: computing-software.software-engineering.erlang.xref-analysis
name: xref-analysis
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-static-analysis, xref-analysis]
level: practitioner
status: docs-checked
description: "Erlang xref: undefined function calls, unused exports, deprecated calls via rebar3 xref and xref_ignores."
sources:
  - https://www.erlang.org/doc/apps/tools/xref.html
  - https://raw.githubusercontent.com/erlang/rebar3/main/rebar.config.sample
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# xref cross-reference checks
**Goal:** catch missing functions and dead code at build time.

```erlang
{xref_checks, [undefined_function_calls, undefined_functions, locals_not_used,
               exports_not_used, deprecated_function_calls, deprecated_functions]}.
{xref_ignores, [{myapp_cb, handle, 1}]}.
```
```
rebar3 xref
```
- Ignore false positives in-source: `-ignore_xref([{mod, fun, 1}]).`.
- `exports_not_used` is noisy for libraries (public API) and behaviour callbacks; enable it only for closed applications.
- Interactive: `xref:start(s)`, `xref:add_directory(s, "ebin")`, `xref:analyze(s, undefined_function_calls)`.

## Gotchas
- Dynamic calls (`apply/3` with variables) are invisible to xref.

## Self-check
Reference a nonexistent function and see the xref failure.

## Checked

The xref module page confirmed the check names, the `ignore_xref` attribute, `start/1`, `add_directory/2`, `analyze` and that calls to `apply` or `spawn` with variable module, function or arguments are unresolved. The rebar.config.sample confirmed `xref_checks` and `xref_ignores` (module, `{module, function}` or `{module, function, arity}` entries) and mentions "rebar3 xref analysis". The claim that `exports_not_used` is noisy for libraries is author advice; the module page only defines the check.

Method: docs-checked 2026-11-09 against erlang.org/doc/apps/tools xref module page and rebar3 rebar.config.sample (xref section).
