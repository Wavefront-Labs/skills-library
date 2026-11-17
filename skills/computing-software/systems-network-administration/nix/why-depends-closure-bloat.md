---
id: computing-software.systems-network-administration.nix.why-depends-closure-bloat
name: why-depends-closure-bloat
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, why-depends, closure-size, runtime-references, build-time-dependencies]
level: advanced
status: docs-checked
description: "Find out why one store path depends on another with nix why-depends, hunt unwanted references that bloat a closure and show build-time links with --derivation."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/src/nix/why-depends.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
How Nix finds dependencies: it scans files for the hash part of store paths. If a file in one path contains another path's hash, the first references the second and may need it at runtime. The full transitive closure of references is kept, so a path cannot be installed without them.

Unwanted references (for example a compiler referenced from a binary) bloat closure size. `nix why-depends` shows a shortest reference chain from the package to the dependency and, per step, a file fragment containing the reference.

```
nix why-depends nixpkgs#hello nixpkgs#glibc
nix why-depends --all nixpkgs#thunderbird nixpkgs#xorg.libX11
nix why-depends --derivation nixpkgs#geeqie nixpkgs#systemd
```

- `--all`: all paths and files in the dependency graph, not just one chain.
- `--derivation`: build-time rather than runtime dependencies between derivations.

## Checked

2026-11-04: hash-scanning mechanism, closure guarantee, bloat description, shortest-chain output, --all and --derivation and the example commands confirmed against the nix why-depends manual page. Removed the pairing advice (requisites, disallowedReferences) and the Verify line, which the page does not state.

Method: documentation only; no commands were run.
