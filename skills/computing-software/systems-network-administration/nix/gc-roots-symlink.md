---
id: computing-software.systems-network-administration.nix.gc-roots-symlink
name: gc-roots-symlink
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, gc-roots, gcroots, indirect-roots]
level: advanced
status: docs-checked
description: "Pin a store path against the Nix garbage collector by symlinking it under the gcroots directory; how recursive search and non-store symlinks are treated."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/package-management/garbage-collector-roots.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Store paths with a symlink pointing to them in `prefix/nix/var/nix/gcroots` are garbage collector roots.

```
ln -s /nix/store/d718ef...-foo /nix/var/nix/gcroots/bar
```

(Truncated hash and names are the manual's example.)

After this the collector will not remove `/nix/store/d718ef...-foo`, and it also keeps that path's dependencies.

Rules:
- Subdirectories of the gcroots directory are searched recursively.
- Symlinks to store paths count as roots.
- Symlinks to non-store paths are ignored, unless the non-store path is itself a symlink to a store path.

## Checked

2026-11-04. Confirmed against the Nix manual Garbage Collector Roots page: the gcroots directory, the `ln -s` example, recursive search of subdirectories, and the symlink rules. Removed an interpretation about indirect roots and `nix-build` result links, an unsourced gotcha, and a verify step the page does not state.

Method: documentation only; no commands were run.
