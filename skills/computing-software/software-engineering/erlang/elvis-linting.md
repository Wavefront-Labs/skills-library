---
id: computing-software.software-engineering.erlang.elvis-linting
name: elvis-linting
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-static-analysis, elvis-linting]
level: practitioner
status: draft
description: "Erlang code linting with elvis: elvis.config rulesets, rebar3_lint plugin, common rules and CI use."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Linting with elvis
**Goal:** enforce team style automatically.

```erlang
%% elvis.config
[{elvis, [{config, [#{dirs => ["src", "test"],
                      filter => "*.erl",
                      ruleset => erl_files}]}]}].
```
```
rebar3 lint        # with project_plugins: [rebar3_lint]
```
- Rules include line length, no tabs, naming conventions, no trailing whitespace, no `export_all`; each can be tuned or disabled per config.
- Rule names and defaults change between elvis versions (unconfirmed list); check the version you pin.
- Run lint after format so style rules and formatter agree.

## Gotchas
- Lint rules that fight your formatter produce churn; align them first.

## Self-check
Run `rebar3 lint` on a file with a tab and confirm it is reported.
