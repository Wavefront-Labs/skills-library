---
id: computing-software.software-engineering.erlang.macros-preprocessor
name: macros-preprocessor
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-lexical, macros-preprocessor]
level: practitioner
status: docs-checked
description: "Erlang preprocessor: -define, -include, -include_lib, -ifdef, predefined macros such as ?MODULE and TEST."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Macros, includes and conditional compilation
**Goal:** use the preprocessor without hiding logic.

```erlang
-define(TIMEOUT, 5000).
-define(LOG(Fmt, Args), io:format(Fmt ++ "~n", Args)).
-include("records.hrl").                       % searched in cwd, module dir, then include dirs
-include_lib("kernel/include/file.hrl").       % first path part is an application name
-ifdef(DEBUG).
-define(TRACE(X), io:format("~p~n", [X])).
-endif.
f() -> ?LOG("in ~p:~p/~p", [?MODULE, ?FUNCTION_NAME, ?FUNCTION_ARITY]).
```
- Predefined: `?MODULE`, `?MODULE_STRING`, `?FILE`, `?LINE`, `?FUNCTION_NAME`, `?FUNCTION_ARITY`, `?OTP_RELEASE` (OTP 21+).
- `-undef(NAME).`, `-ifndef`, `-else.`, `-if(Cond).` and `-elif(Cond).` also exist (for example `-if(?OTP_RELEASE >= 26).`).
- `-include` searches the current directory, the directory of the module, then the `include` option directories; `-include_lib` takes an application name as the first component and finds it via `code:lib_dir/1`.
- Define from the command line with `erlc -DName` or `-DName=Value`.

## Gotchas
- Prefer functions unless you need `?LINE`, `?FUNCTION_NAME` or compile-time constants.

## Self-check
Compile with and without `-DDEBUG` and confirm the guarded block appears only with it.

## Checked
2026-11-02. Erlang Reference Manual "Preprocessor" (include search order, include_lib, predefined macros, OTP 21 `?OTP_RELEASE`, undef/ifdef/ifndef/else/if/elif), ERTS `erlc` manual (`-D`). Removed: rebar3 `{d,...}` and automatic `TEST` define claims, the `-compile(export_all)`-under-TEST example, and the "unhygienic macros" aside (not in these pages).
Method: documentation only; no commands were run.
