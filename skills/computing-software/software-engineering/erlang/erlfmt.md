---
id: computing-software.software-engineering.erlang.erlfmt
name: erlfmt
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-style, erlfmt]
level: practitioner
status: draft
description: "Erlang code formatting with erlfmt: CLI -w and -c, rebar3 fmt plugin, line length and CI check."
sources:
  - https://www.erlang.org/doc/apps/stdlib/
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Formatting with erlfmt
**Goal:** make formatting automatic and uncontroversial.

```
erlfmt -w "src/*.erl" "test/*.erl"     # write formatted files
erlfmt -c "src/*.erl"                  # check only, non-zero exit if not formatted
```
```erlang
{project_plugins, [erlfmt]}.
{erlfmt, [write, {files, ["src/*.erl", "include/*.hrl", "test/*.erl"]}]}.
```
- With the plugin: `rebar3 fmt` (and a check mode; exact flag unconfirmed, see `rebar3 fmt --help`).
- Default print width is 100 columns; configure via pragma or options, but prefer defaults.
- erlfmt preserves a blank line between top-level forms and keeps most line breaks you chose in lists and calls.
- Format in a pre-commit hook and verify in CI.

## Gotchas
- Format in one repo-wide commit and add it to `.git-blame-ignore-revs`.

## Self-check
Run `erlfmt -c` on an unformatted file and check the exit code.
