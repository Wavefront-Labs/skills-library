---
id: computing-software.systems-network-administration.nix.store-verify-and-repair
name: store-verify-and-repair
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, store-verify, check-contents, repair-path, store-corruption]
level: advanced
status: docs-checked
description: "Check Nix database and store consistency with nix-store --verify --check-contents and re-download damaged paths with --repair or --repair-path, safely."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-store/verify.md
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-store/repair-path.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nix-store --verify [--check-contents] [--repair]` checks the internal consistency of the Nix database and between database and store, repairing inconsistencies automatically. These usually come from non-Nix tools changing the store or database, or from bugs.

- `--check-contents`: computes a SHA-256 of each valid path and compares it with the hash recorded at build time; modified paths are printed. Slow on large stores.
- `--repair`: restores a missing valid path or one `--check-contents` found modified, by redownloading it.

Single path:

```
nix-store --verify-path /nix/store/<hash>-name
nix-store --repair-path /nix/store/<hash>-name
```

`--verify-path` on a modified path reports expected and actual hashes. `--repair-path` redownloads using available substituters; with no substitutes, repair is not possible.

Warning: repair briefly moves the existing path out of the way. If interrupted in that window the system can be left broken, especially for a critical path such as the GNU C Library.

## Checked

2026-11-04: verify description, --check-contents, --repair, --repair-path, the example and the repair warning confirmed against the nix-store --verify and --repair-path manual pages. Removed the advice about unstable machines and the Verify line, which the pages do not state.

Method: documentation only; no commands were run.
