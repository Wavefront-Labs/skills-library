---
id: computing-software.software-engineering.erlang.rebar-config
name: rebar-config
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-rebar3, rebar-config]
level: practitioner
status: draft
description: "rebar3 project config: erl_opts, deps, profiles, shell, project layout and core commands compile, shell, eunit, ct, dialyzer."
sources:
  - https://rebar3.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# rebar.config structure and commands
**Goal:** configure and drive a rebar3 project.

```erlang
{erl_opts, [debug_info, warnings_as_errors]}.
{deps, []}.
{shell, [{apps, [myapp]}, {config, "config/sys.config"}]}.
{dialyzer, [{warnings, [unmatched_returns, error_handling]}]}.
{xref_checks, [undefined_function_calls, undefined_functions, locals_not_used]}.
{cover_enabled, true}.
```
```
rebar3 new app myapp        # also: lib, release, umbrella
rebar3 compile
rebar3 shell                # app loaded with deps
rebar3 eunit && rebar3 ct
rebar3 do xref, dialyzer
rebar3 clean -a
```
- Layout: `src/`, `include/`, `test/`, `priv/`, `config/`, `_build/` (never commit).
- rebar3 sets `{d, 'TEST'}` and adds `test/` in the test profile.
- Commit `rebar.lock`.

## Gotchas
- `warnings_as_errors` in `erl_opts` also applies to dependencies you build from source unless profile-scoped.

## Self-check
Run `rebar3 new app demo` then `rebar3 compile` in the new folder.
