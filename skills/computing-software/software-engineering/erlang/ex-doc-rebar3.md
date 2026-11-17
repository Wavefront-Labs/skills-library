---
id: computing-software.software-engineering.erlang.ex-doc-rebar3
name: ex-doc-rebar3
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-docs, ex-doc-rebar3]
level: practitioner
status: draft
description: "Building HTML and Hex documentation for Erlang with rebar3_ex_doc configuration and publishing to HexDocs."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ExDoc via rebar3_ex_doc
**Goal:** ship good docs with a library.

```erlang
{project_plugins, [rebar3_ex_doc]}.
{ex_doc, [
  {extras, ["README.md", "LICENSE"]},
  {main, "README.md"},
  {source_url, "https://example.invalid/mylib"}
]}.
```
```
rebar3 ex_doc
rebar3 hex publish
```
- `rebar3 ex_doc` writes HTML to `doc/`; publishing to Hex uploads docs to HexDocs (exact upload command may be `rebar3 hex publish` with docs or `rebar3 hex docs`; unconfirmed).
- Cross-reference with `m:Module`, `t:Type`, `c:Callback` forms in Markdown (per ExDoc auto-link docs).

## Gotchas
- Broken extras paths fail silently in some versions; open the generated index.

## Self-check
Build docs and click a cross-reference.
