---
id: computing-software.systems-network-administration.nix.flake-references
name: flake-references
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, flakes, flake-reference, github-flake, indirect-registry]
level: practitioner
status: docs-checked
description: "Write Nix flake references in attribute-set and URL-like form: github, git, path, tarball and registry (indirect) types, dir, ref and rev."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/src/nix/flake.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A flake reference takes two forms: an attribute set (only `type` is required) or a compact URL-like string used on the command line and in `inputs`.

```
inputs.nixpkgs.url = "github:NixOS/nixpkgs";
```

URL-like examples:
- `nixpkgs`: registry lookup
- `nixpkgs/<rev>`: registry entry with revision overridden
- `github:NixOS/nixpkgs/nixos-20.09`: a branch
- `github:NixOS/nixpkgs/pull/357207/head`: a pull request
- `git+https://github.com/NixOS/patchelf?ref=refs/tags/0.18.0`: a Git tag
- `github:edolstra/nix-warez?dir=blender`: flake in a subdirectory
- `.` or `/path/to/dir`: path-like (a relative path needs a leading `./`)

Types:
- `indirect` (default): registry lookup.
- `path`: local directory.
- `git`, `mercurial`: repositories.
- `tarball`, `file`: archives or single files over HTTP(S) or local disk.
- `github`, `gitlab`, `sourcehut`: forge archives, optional `host` for self-hosted instances.

Common attributes: `dir` (subdirectory containing `flake.nix`), `narHash`, `rev`, `ref`. Locked references may also carry `revCount` and `lastModified`.

Gotcha: in `nix flake update` a flake in a subdirectory needs the `./` prefix, or Nix looks the name up in the registry.

## Checked

2026-11-04. Confirmed against the Nix flake and flake-update manual pages: the two reference forms, the URL-like examples, path-like rules including the mandatory `./`, the types and their defaults, the generic attributes `dir`, `narHash`, `rev`, `ref`, and the `revCount` and `lastModified` locked attributes. Removed an unsourced verify line.

Method: documentation only; no commands were run.
