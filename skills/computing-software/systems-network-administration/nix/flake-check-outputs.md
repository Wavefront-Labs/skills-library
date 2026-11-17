---
id: computing-software.systems-network-administration.nix.flake-check-outputs
name: flake-check-outputs
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, flake-check, checks-output, no-build, keep-going]
level: practitioner
status: docs-checked
description: "Validate a flake with nix flake check: which outputs must be derivations or typed values, deprecated output names, --no-build and keep-going."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/src/nix/flake-check.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nix flake check` verifies that a flake evaluates and that the derivations in its `checks` output build.

```
nix flake check
nix flake check --no-build github:NixOS/patchelf
```

`--no-build` evaluates without building checks, which suits a remote flake. With the `keep-going` option, Nix keeps evaluating and reports errors as found; otherwise it stops at the first error.

Type requirements:
- Must be derivations: `checks`, `devShells`, `nixosConfigurations.<name>.config.system.build.toplevel`, `packages`.
- `apps` must be app definitions, `templates` template definitions, `overlays` Nixpkgs overlays, `nixosModules` NixOS modules, `bundlers` bundlers.
- `hydraJobs` is evaluated like Hydra's `hydra-eval-jobs`, as a nested set of derivations.
- `legacyPackages.<system>` is evaluated like `nix-env --query --available`.

Deprecated names such as `defaultPackage`, `devShell` and `overlay` still work but emit a warning; each has a newer equivalent under `packages`, `devShells`, `overlays` and so on.

## Checked

2026-11-04. Confirmed against the Nix flake-check manual page: the two examples, `--no-build`, the `keep-going` option, the lists of outputs that must be derivations, apps, templates, overlays, NixOS modules and bundlers, the renamed deprecated attributes that warn, and `hydraJobs` and `legacyPackages` evaluation. Removed an unsourced exit-status line.

Method: documentation only; no commands were run.
