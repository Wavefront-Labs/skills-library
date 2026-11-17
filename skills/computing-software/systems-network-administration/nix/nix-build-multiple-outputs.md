---
id: computing-software.systems-network-administration.nix.nix-build-multiple-outputs
name: nix-build-multiple-outputs
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, multiple-outputs, attr-all, output-symlinks]
level: practitioner
status: docs-checked
description: "Build one or all outputs of a multi-output derivation with nix-build --attr pkg.all or pkg.man and understand the result-outputname symlink naming."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-build.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If a derivation has several outputs, `nix-build` builds the default (first) output.

All outputs:

```
nix-build '<nixpkgs>' --attr openssl.all
```

This creates `result`, `result-bin` and `result-man` symlinks. The `-outputname` suffix is omitted for the `out` output.

One non-default output:

```
nix-build '<nixpkgs>' --attr openssl.man
```

This builds just the `man` output and creates `result-man`.

(`openssl` is the manual's example; outputs depend on the derivation.)

A tarball URL can be given as the expression path; the manual builds GNU Hello from the latest Nixpkgs master tarball with `--attr hello`.

Gotchas:
- Every `result*` link is a GC root; remove them (or use `--no-out-link`) when you want the paths collectable.
- `--attr` selects the derivation; the `.all`, `.man` suffixes select outputs of that derivation.

## Checked

2026-11-04. Confirmed against the Nix manual nix-build page: building the default (first) output, `openssl.all` creating `result`, `result-bin` and `result-man`, the omitted `out` suffix, `openssl.man` creating `result-man`, the GC root warning and `--no-out-link`, and the tarball example. Reworded a claim about pinning a revision, which the page does not make, and removed an unsourced verify line.

Method: documentation only; no commands were run.
