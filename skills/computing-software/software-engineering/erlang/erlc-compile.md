---
id: computing-software.software-engineering.erlang.erlc-compile
name: erlc-compile
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-compiler, erlc-compile]
level: practitioner
status: docs-checked
description: "Erlang compiler: erlc flags, compile:file options, warnings_as_errors, debug_info, bin_opt_info, recv_opt_info and S/E listings."
sources:
  - https://www.erlang.org/doc/apps/erts/erlc_cmd.html
  - https://www.erlang.org/doc/apps/compiler/compile.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# erlc and compiler options
**Goal:** compile with the right options and read compiler hints.

```
erlc -o ebin -I include +debug_info +warnings_as_errors src/mymod.erl
erlc +bin_opt_info src/mymod.erl        # binary matching optimisation hints
erlc -S src/mymod.erl                   # assembly listing mymod.S
erlc -E src/mymod.erl                   # source after transformations, mymod.E
```
```erlang
compile:file("src/mymod", [debug_info, return_errors, {outdir, "ebin"}]).
```
- `erlc -I Dir` adds an include search directory, `-o Dir` sets the output directory (default: current directory), `-D<Name>[=<Value>]` defines a macro, `-Werror` makes warnings errors. A flag starting with `+` is converted to an Erlang term and passed to the compiler, e.g. `erlc +export_all file.erl`. `-P`, `-E` and `-S` are the same as `+'P'`, `+'E'`, `+'S'`.
- `S` writes `<File>.S` (assembler listing) and `E` writes `<File>.E` (code after all source transformations); neither produces an object file.
- `debug_info` includes Erlang Abstract Format in the BEAM file; Debugger, Xref and Cover require it. `bin_opt_info` and `recv_opt_info` emit informational warnings about binary matching and selective receive optimisation. `warnings_as_errors` treats warnings as errors; `return_errors` returns `{error, ErrorList, WarningList}`; `{outdir, Dir}` sets the object directory.
- Inlining: `inline` lets the compiler decide; `{inline, [{Name, Arity}]}` inlines calls to the named functions.
- `warn_export_vars` warns about implicitly exported variables used after the primitive that defined them; `nowarn_unused_function` turns off unused local function warnings.

## Self-check
Run `erlc +bin_opt_info` on a binary-parsing module and read the hints.

## Checked

2026-11-03. Confirmed in the `erlc` command page and the `compile` module page (flags and options above). Removed: the rebar3 `erl_opts` example, the Dialyzer claim about `debug_info`, and the `warn_unused_vars` / `warn_shadow_vars` mentions.
Method: documentation only; no commands were run.
