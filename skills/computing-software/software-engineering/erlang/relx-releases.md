---
id: computing-software.software-engineering.erlang.relx-releases
name: relx-releases
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-releases, relx-releases]
level: practitioner
status: docs-checked
description: "Erlang releases with rebar3/relx: relx config, include_erts, extended_start_script, tar packaging and bin/<name> commands."
sources:
  - https://rebar3.org/docs/deployment/releases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building releases with relx
**Goal:** package an app plus ERTS as a self-contained release.

```erlang
{relx, [
  {release, {myapp, "0.1.0"}, [myapp, sasl]},
  {mode, dev},
  {sys_config, "config/sys.config"},
  {vm_args, "config/vm.args"},
  {extended_start_script, true}
]}.
{profiles, [{prod, [{relx, [{mode, prod}]}]}]}.
```
```
rebar3 release
rebar3 as prod tar
_build/prod/rel/myapp/bin/myapp foreground
```
- Modes expand to option sets: `dev` is `dev_mode` true (symlinks), `include_src` true, `debug_info` keep, `include_erts` false. `prod` is `include_src` false, `debug_info` strip, `include_erts` true, `dev_mode` false. `minimal` is `prod` without ERTS. Explicit options override the mode.
- Building with `rebar3 as prod ...` enables relx `prod` mode automatically. A tarball cannot contain `dev_mode` symlinks.
- `include_erts` can be a path instead of a boolean (with `system_libs` a path) to bundle an ERTS built for another system; `false` uses the target's Erlang.
- The tarball is created under `_build/prod/rel/myapp/` as `myapp-0.1.0.tar.gz`; copy it to a compatible system, extract and run `bin/myapp console`.
- `config/sys.config(.src)` and `config/vm.args(.src)` are included automatically if present; otherwise set `sys_config`, `sys_config_src`, `vm_args`, `vm_args_src`. `.src` files substitute `${VAR}` and `${VAR:-default}` at start (default syntax needs Rebar3 3.14.0 or later).
- Start script commands: `foreground`, `console`, `console_clean`, `remote`, `rpc`, `eval`, `status`, `restart` (applications, not VM), `reboot`, `stop`, `pid`, `ping`, `daemon`, `daemon_attach`, plus `unpack`, `install`, `uninstall`, `upgrade`, `downgrade`, `versions` for release_handler. Use `foreground` in production and `remote` to attach to it.
- `<release_vsn>` may be a string, `semver`, `{cmd, ...}`, `{git, short|long}` or `{file, File}`. Build one release with `rebar3 release -n name`.

## Gotchas
- Relx warns when external functions called by release modules are missing from the release (usually an app absent from the dependent's `.app.src`); disable only with `check_for_undefined_functions`.
- Setting only `include_erts` false in a `prod` tarball still bundles `kernel` and `stdlib` unless `system_libs` is also false (or mode `minimal`).
- If `app_vsn` is given in a release app tuple it must match `.app.src`.

## Self-check
Build a prod tarball, extract it elsewhere, and run `bin/myapp foreground`.

## Checked
Method: docs-checked 2026-11-09 against https://rebar3.org/docs/deployment/releases/ (read in full). Dropped the unconfirmed glibc/musl claim and the claim that `rebar3 xref` is the fix for missing apps.
