---
id: computing-software.systems-network-administration.nix.flake-lock-file
name: flake-lock-file
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, flake-lock, flake-update, lock-file, nix-flake-lock]
level: practitioner
status: docs-checked
description: "Understand flake.lock structure (root, nodes, original, locked) and use nix flake update versus nix flake lock to bump or only add pinned inputs."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/src/nix/flake.md
  - https://raw.githubusercontent.com/NixOS/nix/master/src/nix/flake-update.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`flake.lock` is a UTF-8 JSON file pinning every input, as a graph:
- `root`: label of the root node.
- `nodes`: each has `inputs`, `original` (spec from `flake.nix`), `locked` (pinned spec) and optionally `flake`.
- The root node has no `original` or `locked`, because changing the lock file would change its hash.

Locked attributes are final: they are the only values passed to `outputs` and must agree with what the fetcher returns. Lock files may contain circular dependencies between flakes. If a lock file is up to date, Nix does not read the lock files of dependencies, but generating one does by default.

Commands:

```
nix flake update
nix flake update nixpkgs
nix flake update --flake /path/to/dir
nix flake lock
```

- `nix flake update` with no arguments updates all inputs; it creates the lock file if missing and adds missing inputs.
- Naming inputs updates only those.
- It operates on the flake in the current directory; `--flake` points elsewhere (prefix a relative path with `./`).
- `nix flake lock` creates lock files and adds missing inputs but never updates inputs already locked.

## Checked

2026-11-04. Confirmed against the Nix flake and flake-update manual pages: the UTF-8 JSON lock file, `root`, `nodes`, `original`, `locked` and `flake`, the root node omitting `original` and `locked`, locked attributes being final, circular dependencies, the dependency lock-file behaviour, and the `nix flake update` and `nix flake lock` semantics including `--flake`. Removed an unsourced verify line.

Method: documentation only; no commands were run.
