---
id: computing-software.systems-network-administration.nix.nix-run-app
name: nix-run-app
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-run, flake-apps, main-program, installable]
level: intro
status: docs-checked
description: "Run a flake app or package binary with nix run, pass arguments after --, understand which binary is chosen and define an apps output."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/src/nix/run.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nix run` builds and runs an installable that evaluates to an app or a derivation. For a derivation it runs `<out>/bin/<name>`, where the name comes from `meta.mainProgram`, `pname`, or the name part of `name`, in that order.

```
nix run nixpkgs#vim
nix run nixpkgs#vim -- --help
nix run . -- arg1 arg2
nix run blender-bin#blender_2_83
```

Arguments go after `--`. The first positional argument is always the installable, so to give arguments to the default one, name it explicitly (as `.` above). `nix flake show <flake>` lists available apps.

Lookup order:
- No attribute: `apps.<system>.default`, then `packages.<system>.default`.
- With a name: `apps.<system>.<name>`, `packages.<system>.<name>`, `legacyPackages.<system>.<name>`.

An app is a flake output at `apps.<system>.<name>` with:
- `type` (required): `"app"`.
- `program` (required): full path to the executable, which must be in the Nix store.
- `meta.description` (optional).

## Checked

2026-11-04: binary selection order, argument handling, flake output lookup order and the app attributes confirmed against the nix run manual page. Removed the Verify line, which the page does not state.

Method: documentation only; no commands were run.
