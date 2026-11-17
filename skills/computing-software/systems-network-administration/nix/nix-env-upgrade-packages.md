---
id: computing-software.systems-network-administration.nix.nix-env-upgrade-packages
name: nix-env-upgrade-packages
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-env-upgrade, version-comparison, always-flag, downgrade]
level: practitioner
status: docs-checked
description: "Upgrade installed packages with nix-env --upgrade; choose --lt, --leq, --eq or --always and understand how Nix splits and orders package versions."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-env/upgrade.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```
nix-env --upgrade --attr nixpkgs.gcc
nix-env --upgrade gcc-3.3.2 --always
nix-env --upgrade
```

`-A` is preferred: faster and unambiguous. Paths without a newer version are left alone, and an argument matching no installed derivation is not an error. If several store paths share a symbolic name, only the highest version is installed.

Flags:
- `--lt` (default): only newer versions.
- `--leq`: also same version; forces installed and available to sync, since versions do not uniquely identify a derivation.
- `--eq`: only same version; rebuild installed apps against newer dependencies after a new Nixpkgs release.
- `--always`: newer, same or lower, so packages may be downgraded.
- `--prebuilt-only` / `-b`, `--preserve-installed` / `-P` as for install.

Versions: `y` upgrades `x` if names match and `y` is higher. The name splits at the first dash not followed by a letter (`gcc-3.3.1` gives `gcc` and `3.3.1`). Versions split into number and letter runs compared left to right: numbers as integers, empty below number, `pre` below other components, strings below numbers.

Examples: `2.3.1 > 2.3`, `2.3pre1 < 2.3`, `2.3pre3 < 2.3pre12`, `2.3a < 2.3c`.

## Checked

2026-11-04: flags, no-error behaviour, version splitting and comparison rules and examples confirmed against the nix-env --upgrade manual page. Removed nothing.

Method: documentation only; no commands were run.
