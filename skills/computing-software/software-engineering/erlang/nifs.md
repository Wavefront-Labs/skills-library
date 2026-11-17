---
id: computing-software.software-engineering.erlang.nifs
name: nifs
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-native, nifs]
level: sme
status: draft
description: "Erlang NIFs: erlang:load_nif, on_load, enif_* API, ERL_NIF_INIT, dirty CPU/IO flags and resource objects."
sources:
  - https://www.erlang.org/doc/apps/erts/
  - https://www.erlang.org/doc/apps/erl_interface/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NIFs and dirty schedulers
**Goal:** understand when and how to write a NIF.

```erlang
-module(fastmath).
-export([add/2]).
-nifs([add/2]).
-on_load(init/0).
init() -> erlang:load_nif(filename:join(code:priv_dir(myapp), "fastmath"), 0).
add(_, _) -> erlang:nif_error(nif_not_loaded).
```
```c
#include <erl_nif.h>
static ERL_NIF_TERM add(ErlNifEnv* env, int argc, const ERL_NIF_TERM argv[]) {
    int a, b;
    if (!enif_get_int(env, argv[0], &a) || !enif_get_int(env, argv[1], &b)) return enif_make_badarg(env);
    return enif_make_int(env, a + b);
}
static ErlNifFunc funcs[] = {{"add", 2, add, 0}};
ERL_NIF_INIT(fastmath, funcs, NULL, NULL, NULL, NULL)
```
- A NIF that runs more than about 1 ms blocks a scheduler; mark long work `ERL_NIF_DIRTY_JOB_CPU_BOUND` or `ERL_NIF_DIRTY_JOB_IO_BOUND` in the flags field.
- A crash or memory error in a NIF kills the whole VM. Prefer ports or a separate OS process when isolation matters.
- Resource objects (`enif_alloc_resource`, `enif_make_resource`, `enif_release_resource`) tie native memory to GC.

## Gotchas
- Build for the same OS, architecture and libc as the release.
- Rust bindings (rustler) exist; their API is not covered here.

## Self-check
Build the library, load the module, call `fastmath:add(1, 2)`.
