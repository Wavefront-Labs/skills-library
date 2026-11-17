---
id: computing-software.software-engineering.haskell.cross-compilation-and-releases
name: cross-compilation-and-releases
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, cross-compile, ghc-cross, windows-release, macos-universal, github-actions, haskell-actions-setup, release-binaries, ghcup-cross, cross-compilation-and-releases]
level: sme
status: draft
description: "Produce release binaries for Linux, macOS and Windows with CI matrices (haskell-actions/setup), static builds, and the limits of GHC cross compilation."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Release binaries

**Goal:** distribute executables for multiple platforms.

## Pragmatic approach: build natively per platform
GitHub Actions matrix over `ubuntu`, `macos`, `windows`:
```yaml
jobs:
  build:
    strategy:
      matrix: { os: [ubuntu-latest, macos-latest, windows-latest], ghc: ['9.6.6'] }
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: haskell-actions/setup@v2
        with: { ghc-version: '${{ matrix.ghc }}', cabal-version: 'latest' }
      - uses: actions/cache@v4
        with:
          path: |
            ~/.cabal/packages
            ~/.cabal/store
            dist-newstyle
          key: ${{ runner.os }}-${{ matrix.ghc }}-${{ hashFiles('**/*.cabal', 'cabal.project*') }}
      - run: cabal build --enable-tests && cabal test
      - run: cabal install exe:myapp --install-method=copy --installdir=out
      - uses: actions/upload-artifact@v4
        with: { name: myapp-${{ matrix.os }}, path: out }
```
(Action versions shown are examples; pin to current releases.) On Windows the cabal store path differs (under `%APPDATA%` or a custom directory); cache accordingly.

## Cross compilation
GHC supports cross-compiling with a cross-built compiler (`ghc` configured with `--target`); the practical routes are:
- Nix `pkgsCross` / haskell.nix (Windows via mingw, Linux ARM/musl).
- Zig/clang toolchains, GHC's JavaScript and WebAssembly back ends (newer GHC releases; support evolving, check the release notes).
- TemplateHaskell during cross builds needs an external interpreter (`-fexternal-interpreter`) and is a common problem.

## Release hygiene
- Tag, build, `sha256sum` artifacts, sign, attach to a release.
- Strip binaries, include `LICENSE`, version info (`--version` from `Paths_pkg`), and changelog.
- macOS: universal binaries via `lipo` on separately built arm64 and x86_64 binaries; notarisation required for distribution outside App Store flows.

## Gotchas
- `Paths_<pkg>` data-file lookup breaks for relocated binaries; embed data with `file-embed` or use `getDataFileName` with `<pkg>_datadir` env override.
- Windows executables need shared DLLs for some C libraries; ship them or link statically.

## Self-check
- [ ] Fresh VM runs the artifact without Haskell installed.
- [ ] Checksum and version printed by the binary match the tag.
