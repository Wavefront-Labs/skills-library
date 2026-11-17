---
id: computing-software.software-engineering.erlang.code-paths-loading
name: code-paths-loading
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-code, code-paths-loading]
level: practitioner
status: draft
description: "Erlang code server: code path, -pa/-pz, ERL_LIBS, interactive vs embedded mode, which, lib_dir and priv_dir."
sources:
  - https://www.erlang.org/doc/apps/kernel/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Code paths, loading modes and priv_dir
**Goal:** control where code loads from.

```
erl -pa _build/default/lib/*/ebin
```
```erlang
code:which(lists),              % path of the beam file
code:lib_dir(myapp),            % application directory
code:priv_dir(myapp),           % use for bundled assets and NIF libraries
code:add_patha("/path/ebin"), code:get_path().
```
- `-pa` prepends and `-pz` appends to the code path; `ERL_LIBS` lists directories of applications.
- Interactive mode loads modules on demand (default for plain `erl`); embedded mode (`-mode embedded`) loads all modules at boot and fails fast on missing code. Releases choose via the start script.
- Module resolution failures show as `undef`; `code:which(Mod)` returns `non_existing` if not found.

## Gotchas
- A stale `ebin` earlier in the path shadows your new build.

## Self-check
Check `code:which(mymod)` before and after changing the path.
