---
id: computing-software.systems-network-administration.nix.nix-store-realise
name: nix-store-realise
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-store-realise, realise, read-log, check-flag]
level: practitioner
status: docs-checked
description: "Build or fetch derivations and store paths with nix-store --realise, preview with --dry-run, rebuild with --check and read a build log with --read-log."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-store/realise.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nix-store --realise` (`-r`) builds or fetches store objects: `nix-store --realise paths... [--dry-run]`.

Behaviour:
- Store derivation: substitute the derivation file if invalid, try to fetch outputs from substituters, build the rest (realising dependencies, then running the builder).
- Plain store path not valid: try to fetch its closure from substituters.
- No substitute and no derivation: realisation fails.
- Resulting paths print on standard output.

Options:
- `--dry-run`: print to standard error what would be built or downloaded.
- `--ignore-unknown`: silently skip non-derivation paths without a substitute.
- `--check`: rebuild and verify the result is bitwise-identical to existing outputs, which must already exist; with `-K` a mismatch is kept at `/nix/store/name.check`.

```
nix-store --realise $(nix-instantiate ./test.nix)
nix-build '<nixpkgs>' --attr hello --check -K
nix-store --read-log $(nix-instantiate ./test.nix)
```

The first is essentially what `nix-build` does.

## Checked

2026-11-04: per-path behaviour, failure case, output printing, --dry-run, --ignore-unknown, --check with -K and the three examples confirmed against the nix-store --realise manual page. Removed the Verify line, which the page does not state.

Method: documentation only; no commands were run.
