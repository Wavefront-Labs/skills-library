---
id: computing-software.systems-network-administration.nix.check-build-determinism
name: check-build-determinism
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-build-check, determinism, keep-failed]
level: advanced
status: docs-checked
description: "Spot-check that a derivation builds deterministically with nix-build --check, read the exit status and keep the second output with --keep-failed."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/advanced-topics/diff-hook.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--check` rebuilds a derivation and compares the result with the existing store path. The derivation must already be built.

```
nix-build ./deterministic.nix --attr stable --check
```

Deterministic: exit status 0. Non-deterministic: exit status 1 with

```
error: derivation '/nix/store/...-unstable.drv' may not be deterministic: output '/nix/store/...-unstable' differs
```

Keep the second build's output for inspection:

```
nix-build ./deterministic.nix --attr unstable --check --keep-failed
```

Nix reports the `.check` path alongside the original output.

Notes:
- Check paths are not protected from garbage collection and may be deleted at the next collection. The path stays while the `diff-hook` runs but can vanish afterwards, so automation should use the hook or handle missing check paths.
- If the derivation has not been built, `--check` fails with "some outputs ... are not valid, so checking is not possible". Build without `--check` first.

Verify: `echo $?` after the command.

## Checked

2026-11-04. Confirmed against the Nix manual Verifying Build Reproducibility page: `--check` on an existing store path, exit status 0 or 1, the "may not be deterministic" error, `--keep-failed` with the `.check` path, the garbage-collection note, and the "not valid, so checking is not possible" error. Nothing removed.

Method: documentation only; no commands were run.
