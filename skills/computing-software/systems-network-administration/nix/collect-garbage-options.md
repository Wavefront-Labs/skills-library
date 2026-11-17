---
id: computing-software.systems-network-administration.nix.collect-garbage-options
name: collect-garbage-options
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, delete-older-than, max-freed, profile-locations]
level: practitioner
status: docs-checked
description: "Use nix-collect-garbage with -d, --delete-older-than and --max-freed, know it can delete other users' generations, and where it looks for profiles."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-collect-garbage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nix-collect-garbage` is mostly an alias for `nix-store --gc`, plus options that first delete old profile generations (profiles are GC roots, so this frees more).

```
nix-collect-garbage -d
nix-collect-garbage --delete-older-than 30d
nix-collect-garbage --max-freed 1G
```

Options:
- `--delete-old` / `-d`: delete all old generations of each found profile; equals `nix-env --delete-generations old`.
- `--delete-older-than period`: for example `30d`; generations active at that point in time are kept; equals `nix-env --delete-generations <period>`.
- `--max-freed bytes`: stop once at least that many bytes are freed; accepts `K`, `M`, `G`, `T` suffixes.
- `--dry-run` appears in the synopsis.

Warnings: deleting previous configurations makes rollback to them impossible, and these flags can delete generations used by other users on the system.

Profiles are searched in the default profile locations, plus deprecated, unstable paths under `$NIX_STATE_DIR/profiles` and `$NIX_STATE_DIR/profiles/per-user`, kept for migration.

## Checked

2026-11-04. Confirmed against the Nix manual nix-collect-garbage page: synopsis including `--dry-run`, `-d` and `--delete-old`, `--delete-older-than` with the `30d` example, `--max-freed` with K/M/G/T suffixes, the rollback and other-users warnings, and the profile search locations. Removed an unsourced verify line.

Method: documentation only; no commands were run.
