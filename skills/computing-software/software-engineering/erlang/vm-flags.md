---
id: computing-software.software-engineering.erlang.vm-flags
name: vm-flags
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-vm, vm-flags]
level: practitioner
status: draft
description: "BEAM emulator flags in erl: +P, +Q, +t, +S, +zdbbl, -noshell, -noinput, -eval, -s init stop and vm.args."
sources:
  - https://www.erlang.org/doc/apps/erts/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# erl command line and emulator flags
**Goal:** pick the VM flags that matter.

```
erl +P 1000000 +Q 65536 +t 2000000 +zdbbl 32768 -noshell -s init stop
```
- Limits: `+P` max processes (default 262144), `+Q` max ports, `+t` max atoms, `+e` max ETS tables (verify names with `erl -man erl` for your version).
- `+zdbbl` distribution buffer busy limit in kilobytes; raise if distribution links show `busy_dist_port` pressure.
- `-noshell`/`-noinput` for services, `-detached` is not for containers, `-eval Expr` evaluates, `-s Mod Fun` calls a function, `-config` selects sys.config, `-boot` selects boot scripts.
- Environment: `ERL_FLAGS`, `ERL_AFLAGS`, `ERL_ZFLAGS` add flags without editing the command line.
- Inspect running values: `erlang:system_info(process_limit)`, `erlang:system_info(atom_limit)`.

## Gotchas
- Flag casing is meaningful (`+s` vs `+S`).
- Flags in `vm.args` apply only to releases that read that file.

## Self-check
Start with `+P 1000` and print `erlang:system_info(process_limit)`.
