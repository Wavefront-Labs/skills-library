---
id: computing-software.software-engineering.erlang.escript
name: escript
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-shell, escript]
level: practitioner
status: docs-checked
description: "Erlang escript: shebang, %%! emulator args line, main/1, exit codes, compile vs interpret mode and escript:script_name."
sources:
  - https://www.erlang.org/doc/apps/erts/escript_cmd.html
  - https://www.erlang.org/doc/apps/stdlib/escript.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# escript and command-line scripts
**Goal:** write runnable Erlang scripts and CLI tools.

```erlang
#!/usr/bin/env escript
%%! -noshell -sname cli
main([Name]) -> io:format("hello ~s~n", [Name]);
main(_) -> io:format("usage: cli NAME~n"), halt(1).
```
- The first line is the interpreter (shebang) line. An argument line starting with `%%!` supplies emulator arguments; the Emacs directive comment, if present, must be on the second line. Set the execute bit (`chmod +x`) to run the script directly; `escript script.escript args` works on all platforms.
- The script must define `main/1`, called with the list of argument strings. A normal return exits with status 0; an exception exits with status 127; `halt(ExitCode)` returns your own code.
- The script is checked before it runs: warnings are printed and the script still runs; errors stop it with status 127. The module and export declarations of `main/1` are optional.
- By default the script is compiled by the Erlang compiler; before OTP 27 it was interpreted by default. `-mode(interpret)` forces interpretation, which is slower and does not support some constructs but needs no compiler application.
- `escript:script_name/0` returns the script path (usually, but not always, absolute).

## Gotchas
- A source escript is run by an Erlang installation on the target machine. Precompiled scripts are created with `escript:create/2`, and in them `main/1` must be exported.

## Self-check
Run the script with and without an argument and check the exit code.

## Checked

2026-11-03. Confirmed in the `escript` command page (header lines, `%%!`, `main/1`, exit statuses 0 and 127, `halt/1`, compile versus `-mode(interpret)`, OTP 27 default change, `script_name/0`, precompiled scripts) and the `escript` module page. Fixed: the old text said the default is interpreted and `-mode(compile)` compiles; from OTP 27 it is the reverse. Removed: the rebar3 `escriptize` instructions (not covered by the Erlang docs).
Method: documentation only; no commands were run.
