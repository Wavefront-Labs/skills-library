---
id: computing-software.systems-network-administration.nix.nix-env-install-packages
name: nix-env-install-packages
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-env-install, attr-path, priority, outputs-to-install]
level: practitioner
status: docs-checked
description: "Install packages with nix-env --install by name, attribute path, store path or expression; control priority, preserved installs, prebuilt-only and dry runs."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-env/install.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each run creates a new user environment from the current generation of the active profile.

```
nix-env --install --attr gcc40mips
nix-env --install gcc-3.3.2
nix-env --file '<nixpkgs>' --install --attr hello --dry-run
nix-env --install --from-profile /nix/var/nix/profiles/foo gcc
```

How arguments are read:
- By name (default): looked up in the default Nix expression; same-named installed packages are removed unless `--preserve-installed`. With several matches the highest priority wins (`meta.priority`, lower number is higher priority, default 5), then highest version.
- `--attr` / `-A`: attribute paths; faster and unambiguous. List them with `nix-env --query --available --attr-path`.
- `--from-expression`: arguments are functions called with the default expression.
- `--priority`: set priority for plain store paths.
- Store derivations and paths are realised and installed.
- All outputs install by default; `meta.outputsToInstall` restricts them.

Options: `--prebuilt-only` / `-b` (only derivations with a substitute), `--preserve-installed` / `-P` (keep same-named packages), `--remove-all` / `-r` (like `--uninstall '.*'` first, one transaction).

A dry run reports which paths will be downloaded or built from source.

## Checked

2026-11-04: argument interpretation, priority rules (meta.priority, default 5, higher number is lower priority, then highest version), outputsToInstall and the options confirmed against the nix-env --install manual page. Removed the Verify line, which the page does not state.

Method: documentation only; no commands were run.
