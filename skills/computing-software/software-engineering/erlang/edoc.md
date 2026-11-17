---
id: computing-software.software-engineering.erlang.edoc
name: edoc
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-docs, edoc]
level: practitioner
status: draft
description: "Erlang EDoc: @doc tags in comments, @spec, overview, rebar3 edoc and edoc_opts."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EDoc comments and rebar3 edoc
**Goal:** generate HTML API docs from comments.

```erlang
%% @doc Returns the sum of the list.
%% @param L list of numbers
%% @returns the total
%% @end
-spec sum([number()]) -> number().
sum(L) -> lists:sum(L).
```
```
rebar3 edoc
```
- Tags: `@doc`, `@author`, `@version`, `@since`, `@deprecated`, `@see`, `@type`, `@param`, `@returns`, `@throws`, `@equiv`.
- Specs are picked up from `-spec` automatically, so `@spec` is redundant.
- Config: `{edoc_opts, [{preprocess, true}]}` in `rebar.config` when macros appear in docs.
- Output goes to `doc/`.

## Gotchas
- Unbalanced HTML/XML in doc comments breaks generation; keep markup simple.

## Self-check
Run `rebar3 edoc` and open `doc/index.html`.
