---
id: computing-software.systems-network-administration.nix.gc-preview-and-keep-settings
name: gc-preview-and-keep-settings
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, print-dead, print-live, keep-outputs, keep-derivations]
level: practitioner
status: docs-checked
description: "Preview what the Nix garbage collector would delete or keep with --print-dead and --print-live, and tune keep-outputs and keep-derivations."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/package-management/garbage-collection.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Preview before deleting:

```
nix-store --gc --print-dead
nix-store --gc --print-live
```

`--print-dead` lists paths that would be deleted; `--print-live` lists paths that would be kept.

Settings in the Nix configuration file that affect collection:
- `keep-derivations` (default `true`): keeps derivations that are build-time dependencies of garbage collector roots.
- `keep-outputs` (default `false`): keeps output paths that are runtime dependencies. Enabling it can help while developing, since rebuilds stay fast.

Example `nix.conf` for a developer machine:

```
keep-outputs = true
```

With the defaults, everything not covered by these rules and not reachable from a root is collected.

## Checked

2026-11-04. Confirmed against the Nix manual Garbage Collection page: `--print-dead` and `--print-live`, `keep-derivations` default true, `keep-outputs` default false, and their meanings. Removed an unsourced gotcha about store growth and a verify step.

Method: documentation only; no commands were run.
