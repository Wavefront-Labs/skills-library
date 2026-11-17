---
id: computing-software.systems-network-administration.nix.nix-develop-shell
name: nix-develop-shell
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-develop, devshells, build-environment, redirect]
level: practitioner
status: docs-checked
description: "Enter a package's build environment with nix develop, run single build phases, record a profile, redirect a store path and know the devShells lookup order."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/src/nix/develop.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nix develop` starts a `bash` shell with a build environment nearly identical to the one Nix uses to build an installable, so you can build interactively and incrementally.

```
nix develop
nix develop nixpkgs#hello
nix develop --command bash -c 'make'
nix develop --build
```

- In the shell run `configurePhase`, `buildPhase`, `installPhase`, or your own build tools.
- Single phase flags: `--unpack`, `--configure`, `--build`, `--check`, `--install`, `--installcheck`.
- `--command` runs commands non-interactively in the environment.
- `--profile` records the environment so it can be reused by passing the profile path.
- `--redirect` swaps a store path (for example a package's `dev` output) for a writable directory, useful when compiling another package against a modified dependency.

Lookup order:
- No output name: `devShells.<system>.default`, then `packages.<system>.default`.
- With a name: `devShells.<system>.<name>`, `packages.<system>.<name>`, then `legacyPackages.<system>.<name>`.

Prompt settings `bash-prompt`, `bash-prompt-prefix`, `bash-prompt-suffix` go in `nix.conf` or a flake's `nixConfig`.

## Checked

2026-11-04: bash shell, phase flags, --command, --profile, --redirect and the flake output lookup order confirmed against the nix develop manual page. Removed the Verify line about build inputs on PATH, which the page does not state.

Method: documentation only; no commands were run.
