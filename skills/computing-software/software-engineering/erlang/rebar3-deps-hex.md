---
id: computing-software.software-engineering.erlang.rebar3-deps-hex
name: rebar3-deps-hex
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-rebar3, rebar3-deps-hex]
level: practitioner
status: draft
description: "rebar3 deps: Hex packages with version constraints, git deps with tag/branch/ref, rebar.lock and rebar3 upgrade."
sources:
  - https://rebar3.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dependencies from Hex and Git
**Goal:** pin dependencies reproducibly.

```erlang
{deps, [
  {cowboy, "~> 2.10"},                                         % Hex
  {jsx, "3.1.0"},                                              % exact Hex version
  {recon, {git, "https://github.com/ferd/recon.git", {tag, "2.5.6"}}}  % tag shown as an example
]}.
```
- Git refs: `{tag, "..."}`, `{branch, "..."}`, `{ref, "<sha>"}`. Prefer tag or ref over branch.
- `rebar3 tree` shows the dependency tree; `rebar3 upgrade <dep>` updates a lock entry; `rebar3 unlock` removes lock entries.
- `rebar3 update` refreshes the Hex package index.
- Deps needed only for tests go under `{profiles, [{test, [{deps, [meck]}]}]}`.

## Gotchas
- Branch deps move; the lock file records the commit, but a fresh `unlock` takes whatever is current.
- Package names clash across namespaces; use the Hex name consistently.

## Self-check
Add a dep, run `rebar3 compile`, and check `rebar.lock` is created.
