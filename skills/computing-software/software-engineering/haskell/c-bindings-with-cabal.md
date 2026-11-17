---
id: computing-software.software-engineering.haskell.c-bindings-with-cabal
name: c-bindings-with-cabal
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, c-sources, extra-libraries, pkgconfig-depends, include-dirs, cbits, custom-setup, foreign-library, shared-library, c-bindings-with-cabal]
level: advanced
status: draft
description: "Include C sources and link system libraries from cabal (c-sources, extra-libraries, pkgconfig-depends), build foreign-library shared objects, fix linker errors."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/", "https://www.haskell.org/onlinereport/haskell2010/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# C code in cabal packages

**Goal:** build Haskell packages that depend on C code.

```cabal
library
  c-sources:         cbits/helper.c
  cc-options:        -O2 -Wall
  include-dirs:      cbits
  install-includes:  helper.h
  extra-libraries:   z
  pkgconfig-depends: zlib >= 1.2
  extra-lib-dirs:    /opt/lib          -- avoid hard-coded paths; prefer pkg-config
  build-tool-depends: hsc2hs:hsc2hs
```
Use `hsc2hs` files `Foo.hsc` (`#include <x.h>`, `#{size struct stat}`); cabal runs hsc2hs automatically for `.hsc` modules listed in `exposed-modules`.

## Foreign libraries (shared objects)
```cabal
foreign-library hsmylib
  type:           native-shared
  other-modules:  MyLib
  lib-version-info: 1:0:0
```
Build with `cabal build`; a C program links against it; `foreign export` declares the entry points; initialise the RTS (`hs_init`/`hs_exit`) before calls.

## Troubleshooting
- `cannot find -lfoo`: install the dev package and set `extra-lib-dirs` (cabal.project: `extra-lib-dirs: ...`) or `PKG_CONFIG_PATH`.
- `undefined reference to 'sym'`: missing `extra-libraries` or source in `c-sources`.
- Header not found: `include-dirs` (or `extra-include-dirs` in cabal.project).
- Windows: use MSYS2 packages from GHCup's shell (`pacman -S mingw-w64-x86_64-zlib`), with `extra-include-dirs`/`extra-lib-dirs` pointing to the MSYS2 mingw64 prefix.
- Template Haskell with C dependencies needs a shared library or `-dynamic-too`.

## Gotchas
- C++ sources need `cxx-sources` (Cabal 3.0 and later) and `extra-libraries: stdc++`.
- Different `cc-options` per OS via conditionals.
- Do not vendor large C libraries unless licensing and build-time are acceptable.

## Self-check
- [ ] `cabal build` works on a clean machine with documented system dependencies.
- [ ] Linker flags use pkg-config where available.
