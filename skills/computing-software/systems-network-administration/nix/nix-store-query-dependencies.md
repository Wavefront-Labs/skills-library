---
id: computing-software.systems-network-administration.nix.nix-store-query-dependencies
name: nix-store-query-dependencies
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-store-query, requisites, referrers, closure-size]
level: practitioner
status: docs-checked
description: "Inspect store paths with nix-store --query: closures, referrers, deriver, dependency trees and graphs, hashes, sizes and the GC roots keeping a path alive."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-store/query.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nix-store --query` (`-q`) takes at most one query per call; the default is `--outputs`. Symlinks into the store are followed. Common options: `--use-output` (`-u`) runs the query on a derivation's output; `--force-realise` (`-f`) realises arguments first.

Queries:
- `--references`: immediate dependencies. `--requisites` (`-R`): full closure; `--include-outputs` adds existing outputs of derivations.
- `--referrers`: paths in the store that reference these. `--referrers-closure`: everything referencing them directly or indirectly.
- `--deriver` (`-d`): the derivation, or `unknown-deriver`. `--valid-derivers`: `.drv` files that should produce the path (may be empty).
- `--graph` (Graphviz dot), `--graphml`, `--tree` (ASCII tree by descending closure size, each path expanded once). On a derivation they show build-time dependencies, on an output the runtime ones.
- `--binding name` (`-b`): value of a derivation attribute; error if missing.
- `--hash`: SHA-256 of contents as from `nix-store --dump` (fast, stored in the database). `--size`: bytes of contents; disk use may be higher.
- `--roots`: GC roots that keep the path alive.

Examples: runtime closure of a program with `nix-store -qR $(which svn)`; the GC roots that point at a path with `nix-store -q --roots <path>`; visualise with `--graph` piped to `dot -Tps`.

## Checked

2026-11-04: single-query rule, default --outputs, symlink handling, every query listed, the --graph/--tree/--graphml build-time versus runtime note and the examples confirmed against the nix-store --query manual page. Reworded the --roots example to what the page states.

Method: documentation only; no commands were run.
