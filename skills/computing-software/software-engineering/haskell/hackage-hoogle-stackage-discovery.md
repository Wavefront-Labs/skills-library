---
id: computing-software.software-engineering.haskell.hackage-hoogle-stackage-discovery
name: hackage-hoogle-stackage-discovery
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, hackage, hoogle, stackage, haskell-search, package-quality, reverse-dependencies, haddock-docs, hackage-hoogle-stackage-discovery, haskell-ecosystem]
level: intro
status: draft
description: "Find and vet Haskell libraries: Hoogle type search, Hackage package pages and reverse dependencies, Stackage membership, and package quality signals."
sources: ["https://hackage.haskell.org/", "https://www.stackage.org/", "https://hoogle.haskell.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Discovering and vetting packages

**Goal:** find the right library function or package quickly and judge its health.

## Tools
- **Hoogle** (hoogle.haskell.org): search by name or type, e.g. `[a] -> Int` or `(a -> b) -> [a] -> [b]`; local copy: `cabal install hoogle`, `hoogle generate`, `hoogle search 'Map k v -> [k]'`.
- **Hackage** (hackage.haskell.org): package page, versions, Haddock, changelog, bounds, reverse dependencies, build matrix (are the docs and builds green?). Search by tag or keyword.
- **Stackage** (stackage.org): curated sets of packages that build together (LTS and Nightly); a package listed in an LTS is a good sign of maintenance.
- **Haskell Discourse**, Reddit r/haskell, "haskell.foundation" tooling pages, and `awesome-haskell` lists for survey articles.

## Vetting checklist
1. Recent uploads and bounds supporting current GHC/base.
2. Reverse dependencies from well-known packages (popularity and stability signal).
3. Documentation: Haddock coverage, examples, changelog.
4. Dependencies footprint (`cabal build --dry-run` or `cabal-plan`): fewer is better for libraries.
5. License (BSD-3-Clause, MIT, Apache-2.0, GPL/LGPL implications).
6. Tests present, issue tracker responsive, CI badge.

## Gotchas
- Names suggest nothing: check what a package really does (`mtl` vs `transformers`, `lens` vs `microlens`, `text` vs `text-short`).
- Type-based search needs correct type variable shapes; Hoogle shows `package:module` so import from where the type lives.
- Abandoned packages may still be on Stackage for a while; check last release date.
- Prefer boot packages and Stackage LTS packages for applications.

## Self-check
- [ ] Hoogle search tried before writing a utility.
- [ ] Chosen packages are in the target LTS (`stack build` resolves without extra-deps) or show recent releases.
