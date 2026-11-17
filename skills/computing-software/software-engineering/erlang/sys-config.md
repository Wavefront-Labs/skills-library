---
id: computing-software.software-engineering.erlang.sys-config
name: sys-config
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-config, sys-config]
level: practitioner
status: docs-checked
description: "Erlang sys.config term file and vm.args for rebar3 releases: structure, precedence, include files, node name and cookie."
sources:
  - https://www.erlang.org/doc/apps/kernel/config.html
  - https://rebar3.org/docs/deployment/releases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sys.config and vm.args
**Goal:** configure a release without recompiling.

```erlang
%% config/sys.config
[{myapp, [{port, 8080}, {db, [{host, "localhost"}]}]},
 {kernel, [{logger_level, info}]}].
```
```
## config/vm.args
-name myapp@127.0.0.1
-setcookie myapp
```
- A config file holds a single Erlang term ending in a period: a list of `{Application, [{Par, Val}]}`. Values are read with `application:get_env/1,2`.
- Precedence: config file values override the application resource file (`.app`); command-line flags override the config file. If a parameter appears in several `-config`/`-configfd` sources, the last one read wins.
- `erl -config Name` reads `Name.config` (extension may be omitted).
- In embedded mode / releases exactly one `sys.config` is expected, in `$ROOT/releases/Vsn`; release handling reads the new one on upgrade. To pull in other files, list them as string entries inside `sys.config` (include files); relative paths are looked up beside `sys.config` first, then in the emulator working directory; absolute paths are recommended. Entries are merged: new parameters added, existing ones overwritten.
- rebar3/relx: `config/sys.config` or `config/sys.config.src` and `config/vm.args` or `config/vm.args.src` in the project are included automatically (`.src` wins if both exist). The generated default `vm.args` sets a node name and cookie (`-name <release>@127.0.0.1`, `-setcookie <release>`). Other file names need `{sys_config, ...}`/`{sys_config_src, ...}` or `{vm_args, ...}`/`{vm_args_src, ...}` in the `relx` config.
- Check syntax: `file:consult("config/sys.config")`.

## Gotchas
- A missing final period breaks the term; with include files the runtime aborts at startup if an included file is missing or erroneous, whereas a release upgrade ignores a bad include file with an error message.
- Do not commit real secrets in sys.config or the cookie in vm.args.

## Self-check
Run `{ok, _} = file:consult("config/sys.config")` in CI.

## Checked
Method: docs-checked 2026-11-09 against the Erlang kernel `config` reference page and the rebar3 Releases page (runtime configuration). Dropped the specific emulator flags (+K, +S, +P, +zdbbl) and the logger_level setting, which neither page documents.
