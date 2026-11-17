---
id: computing-software.systems-network-administration.nix.garbage-collect-store
name: garbage-collect-store
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, garbage-collection, delete-generations, nix-collect-garbage]
level: practitioner
status: docs-checked
description: "Reclaim Nix store space: delete old generations, then run the garbage collector, or use nix-collect-garbage -d for a quick cleanup of all profiles."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/package-management/garbage-collection.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Removing a package from a profile (`nix-env -u`, `nix-env -e`) does not free disk space; the package stays in the store.

1. Delete old generations. Old ones keep their packages alive, so this is only safe if you will not roll back.

```
nix-env --delete-generations old
nix-env --delete-generations 10 11 14
nix-env --delete-generations 14d
```

The first removes all non-current generations of the current profile; the second specific ones; the third those older than 14 days (the current one is kept).

2. Run the collector:

```
nix-store --gc
```

It removes store paths that no generation of any profile uses, directly or indirectly.

Quick cleanup: `-d` (`--delete-old`) deletes all old generations of all profiles in `/nix/var/nix/profiles`, then collects.

```
nix-collect-garbage -d
```

To preview what would go, see the preview skill (`--print-dead`).

## Checked

2026-11-04. Confirmed against the Nix manual Garbage Collection page: the `nix-env --delete-generations` forms (`old`, a list, `14d`), `nix-store --gc`, `nix-collect-garbage -d` and its `/nix/var/nix/profiles` scope, and that `nix-env -u` and `-e` do not free space. Removed an unsourced `df` verify step.

Method: documentation only; no commands were run.
