---
id: computing-software.software-engineering.erlang.rebar3-plugins-profiles
name: rebar3-plugins-profiles
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-rebar3, rebar3-plugins-profiles]
level: advanced
status: draft
description: "rebar3 plugins and profiles: project_plugins, global plugins, test and prod profiles, rebar3 as <profile>, overrides."
sources:
  - https://rebar3.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plugins and profiles
**Goal:** separate dev, test and prod builds.

```erlang
{project_plugins, [erlfmt, rebar3_proper, rebar3_lint]}.
{plugins, [rebar3_hex]}.
{profiles, [
  {test, [{deps, [meck, proper]}, {erl_opts, [nowarn_export_all]}]},
  {prod, [{relx, [{mode, prod}, {include_src, false}]}]}
]}.
```
- `project_plugins` are not inherited when the project is a dependency; `plugins` are.
- Run under a profile: `rebar3 as prod release`, `rebar3 as test shell`. Chain: `rebar3 as test,prod compile`.
- Output goes to `_build/<profile>/`; test profile is implicit for `eunit` and `ct`.
- `{overrides, [...]}` adjusts a dependency's build config.

## Gotchas
- `{mode, prod}` copies code, not symlinks, and strips source; dev mode symlinks `_build` lib dirs.

## Self-check
Run `rebar3 as prod compile` and confirm a `_build/prod` directory appears.
