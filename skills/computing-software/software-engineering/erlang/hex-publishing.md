---
id: computing-software.software-engineering.erlang.hex-publishing
name: hex-publishing
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-hex, hex-publishing]
level: practitioner
status: draft
description: "Publishing an Erlang library to Hex with rebar3 hex: metadata, auth, publish, docs and retire."
sources:
  - https://rebar3.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Publishing packages to Hex
**Goal:** ship a library to Hex.pm.

```erlang
%% src/mylib.app.src needs description, vsn, licenses, links
{licenses, ["Apache-2.0"]}.
{links, [{"GitHub", "https://example.invalid/mylib"}]}.
```
```
rebar3 hex user auth          # or: rebar3 hex user register
rebar3 hex publish            # shows a preview and asks to confirm
rebar3 hex retire mylib 0.1.0 invalid "bad release"
```
- Package files default to `src`, `include`, `priv`, `rebar.config`, `README*`, `LICENSE*`; override with `{files, [...]}` in the `hex` or `pkg` config (name unconfirmed, check `rebar3 hex` docs).
- A published version is immutable (you can retire but not edit it within the grace period rules of Hex).
- Documentation can be published to hexdocs with ex_doc.

## Gotchas
- Do not publish with `git` dependencies: Hex packages may only depend on other Hex packages.
- Keep API keys out of CI logs; use a scoped key.

## Self-check
Run `rebar3 hex publish --dry-run` (confirm flag in `--help`) before the real publish.
