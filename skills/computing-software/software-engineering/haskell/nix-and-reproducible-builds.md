---
id: computing-software.software-engineering.haskell.nix-and-reproducible-builds
name: nix-and-reproducible-builds
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, nix, haskell-nix, nixpkgs, cabal2nix, reproducible-build, flake, haskell-flake, index-state, cachix, nix-and-reproducible-builds]
level: sme
status: draft
description: "Reproducible Haskell builds with Nix (nixpkgs haskellPackages, cabal2nix, haskell.nix, flakes) and pinning index-state and freeze files in non-Nix builds."
sources: ["https://hackage.haskell.org/", "https://www.stackage.org/", "https://hoogle.haskell.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reproducible builds

**Goal:** make the same inputs build the same artifact, on CI and developer machines.

## Without Nix
- `cabal.project.freeze` plus `index-state:` in `cabal.project`; Stack's LTS snapshot plus a pinned `stack.yaml.lock` (generated automatically).
- Pin GHC via ghcup version and CI setup action.
- Docker image with a pinned base and GHC version.

## With Nix
```nix
# flake.nix sketch (nixpkgs.haskellPackages route)
{ inputs.nixpkgs.url = "github:NixOS/nixpkgs/<pinned-rev>";
  outputs = { self, nixpkgs }: let pkgs = nixpkgs.legacyPackages.x86_64-linux; in {
    packages.x86_64-linux.default = pkgs.haskellPackages.callCabal2nix "myapp" ./. {};
    devShells.x86_64-linux.default = pkgs.haskellPackages.shellFor {
      packages = p: [ (p.callCabal2nix "myapp" ./. {}) ];
      nativeBuildInputs = with pkgs; [ cabal-install haskell-language-server ];
    };
  }; }
```
- `cabal2nix . > default.nix` converts a cabal file to a Nix expression.
- **haskell.nix** (input-output-hk) builds from cabal/stack plan files with exact versions, cross compilation and static builds; **haskell-flake** is a flake-parts module for project layout. Behaviours differ by version; read their docs.
- Binary caches (cachix, the project's own) avoid rebuilding GHC and dependencies.

## Gotchas
- nixpkgs `haskellPackages` is one package set (like Stackage) pinned to a GHC; versions may lag behind Hackage; use `overrideCabal`/`doJailbreak` for bounds issues.
- System libraries (zlib, openssl, libpq) must be declared as `buildInputs`.
- Nix on Windows is not supported natively (WSL2 works).
- Cabal inside a Nix shell still uses `~/.cabal` unless configured; set `CABAL_DIR` for isolation.

## Self-check
- [ ] Two clean builds produce the same binary hash (when no timestamps or paths leak).
- [ ] Lock inputs are committed.
