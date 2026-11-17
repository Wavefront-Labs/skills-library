---
id: computing-software.systems-network-administration.nix.tune-cores-and-jobs
name: tune-cores-and-jobs
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, max-jobs, cores, nix-build-cores, oversubscription]
level: practitioner
status: docs-checked
description: "Balance the Nix max-jobs and cores settings so parallel builds neither idle nor oversubscribe the CPU; includes the 24-core worked table."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/advanced-topics/cores-vs-jobs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two settings control CPU use:
- `max-jobs`: how many derivations build at once. Zero stops local builds, though Nix can still substitute from caches and build on remote builders.
- `cores`: a suggestion for how many cores each derivation uses, like `make -j`.

`NIX_BUILD_CORES` takes the value of `cores`; if `cores` is `0` it equals the machine's total core count. Maximum consumed cores is `max-jobs` times `NIX_BUILD_CORES`.

Examples for a 24-core machine:

| max-jobs | cores | max processes | outcome |
|---|---|---|---|
| 1 | 24 | 24 | one build at a time, may underuse |
| 4 | 6 | 24 | four builds, six cores each |
| 12 | 6 | 72 | oversubscribed, context switching |
| 24 | 1 | 24 | never oversubscribed, slow for big jobs |
| 24 | 0 | 576 | very likely oversubscribed |

Set in `nix.conf`:

```
max-jobs = 4
cores = 6
```

A derivation's build script must follow `NIX_BUILD_CORES` to honour the per-build core count. The best balance depends on each builder's workload and hardware.

## Checked

2026-11-04: max-jobs and cores meanings, NIX_BUILD_CORES rule, the multiplication and all five 24-core rows confirmed against the Tuning Cores and Jobs manual page. Removed the advice to try values and watch build times, which the page does not state.

Method: documentation only; no commands were run.
