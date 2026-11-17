---
id: computing-software.systems-network-administration.nix.fixed-output-derivations
name: fixed-output-derivations
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, fixed-output, output-hash, output-hash-mode, content-addressed]
level: advanced
status: docs-checked
description: "Declare fixed-output and floating content-addressed derivations with outputHash, outputHashAlgo and outputHashMode, and tell derivation types apart."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/language/advanced-attributes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Derivation types:
- Input-addressed (default): no extra attributes.
- Fixed-output: requires `outputHash`, `outputHashAlgo` and `outputHashMode`.
- Floating content-addressed: requires `outputHashAlgo`, `outputHashMode` and `__contentAddressed = true`; must not set `outputHash`.

Attributes:
- `outputHash`: expected hash of the single output of a fixed-output derivation; hex, nix32 or SRI.
- `outputHashAlgo`: `"blake3"`, `"sha1"`, `"sha256"`, `"sha512"` or `null`. `null` is only allowed when `outputHash` is SRI.
- `outputHashMode`: how contents are digested: `"flat"` (default), `"recursive"` or `"nar"`, `"text"` (experimental, dynamic-derivations), `"git"` (experimental, git-hashing).
- `__contentAddressed`: boolean, default `false`; needs the `ca-derivations` experimental feature.

Sketch:

```
derivation {
  name = "x";
  system = builtins.currentSystem;
  builder = "/bin/sh";
  args = [ "-c" "echo -n hello > $out" ];
  outputHashAlgo = "sha256";
  outputHashMode = "flat";
  outputHash = "<SRI hash>";
}
```

The manual points to the `nix-hash` command for obtaining a hash of some contents and converting between encodings.

## Checked

2026-11-04. Confirmed against the Nix manual Advanced Attributes page: the three derivation types and their attribute combinations, the `outputHash` encodings, the `outputHashAlgo` values and the `null` rule, the `outputHashMode` values with their experimental features, and `__contentAddressed` with `ca-derivations`. Removed the `nix-prefetch-url` and `--sri` hash advice and a verify line the page does not state.

Method: documentation only; no commands were run.
