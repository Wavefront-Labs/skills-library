---
id: computing-software.systems-network-administration.nix.rollback-and-switch-generation
name: rollback-and-switch-generation
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, rollback, switch-generation, switch-profile]
level: practitioner
status: docs-checked
description: "Undo a bad nix-env change with --rollback, jump to a specific generation, or switch the active profile; a profile that does not exist is created."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/package-management/profiles.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```
nix-env --rollback
nix-env --switch-generation 43
nix-env --list-generations
nix-env --switch-profile /nix/var/nix/profiles/my-profile
nix-env --switch-profile /nix/var/nix/profiles/default
```

(`43` and `my-profile` are the manual's examples.)

- `--rollback` points the current generation back to the previous one.
- `--switch-generation N` switches to a specific generation (the page's example rolls forward to generation 43 again).
- `--list-generations` shows all available generations.
- `--switch-profile` changes the active profile; if the target does not exist it is created.

## Checked

2026-11-04: rollback, switch-generation, list-generations and switch-profile behaviour, including profile creation, confirmed against the Profiles manual page. Removed the Gotcha about deleted generations and the Verify line; the page states neither.

Method: documentation only; no commands were run.
