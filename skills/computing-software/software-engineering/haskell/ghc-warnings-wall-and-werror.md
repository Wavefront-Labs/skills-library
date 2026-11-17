---
id: computing-software.software-engineering.haskell.ghc-warnings-wall-and-werror
name: ghc-warnings-wall-and-werror
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, -wall, -wcompat, -werror, -wextra, -wunused, warning-flags, -wno, -wwarn, -woverloaded, ghc-warnings-wall-and-werror, haskell-warnings]
level: practitioner
status: docs-checked
description: "Configure GHC warnings: -Wall, -Wcompat, -Widentities, -Wredundant-constraints, -Wunused-*, -Werror=..., per-module OPTIONS_GHC and cabal common stanzas."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/using-warnings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GHC warnings

**Goal:** a strict-but-livable warning policy that catches real bugs.

## Groups
- Default warnings are on without flags (`-Wdefault`).
- `-W` (alias `-Wextra`): adds unused binds/matches/imports and incomplete patterns; `-Wall` includes all of `-W` plus name shadowing, missing signatures, type defaults, orphans, unused do-bind, incomplete record updates and incomplete uni-patterns.
- `-Wcompat`: warns about changes planned for future releases (migration help).
- `-Weverything` is a firehose; use it to discover options and then pick, e.g. `-Weverything -Wno-implicit-prelude -Wno-missing-import-lists -Wno-unsafe -Wno-all-missed-specialisations` (a pattern many teams use).

## Recommended starting set
```cabal
ghc-options: -Wall -Wcompat -Widentities -Wincomplete-record-updates
             -Wincomplete-uni-patterns -Wmissing-deriving-strategies
             -Wpartial-fields -Wredundant-constraints -Wunused-packages
```
(`-Wunused-packages` warns about packages passed with `-package`/`-package-id` that were not needed; it interacts poorly with GHCi. Newer GHC already includes `-Wincomplete-record-updates` and `-Wincomplete-uni-patterns` in `-Wall`, so listing them is harmless. Names must exist in your GHC; unknown ones warn under `-Wunrecognised-warning-flags`.)

## Controlling
```haskell
{-# OPTIONS_GHC -Wno-orphans #-}               -- per module
```
```bash
ghc -Wall -Werror=incomplete-patterns Foo.hs     # promote only specific warnings
ghc -Wwarn=unused-imports                        # demote
cabal build --ghc-options=-Werror                 # in CI
```
Warning names without `-W` prefix in flags like `-Werror=` and `-Wno-`. Flags appear in output as `[-Wunused-imports]`.

## Gotchas
- Blanket `-Werror` in a package published to Hackage breaks users on newer GHC; keep it in CI only.
- Deferred type errors (`-fdefer-type-errors`) turn errors into runtime exceptions; use only for exploration.
- `-Wmissing-home-modules` flags modules missing in `other-modules`.
- Unused-do-bind warning is fixed with `_ <- action` or `void action`.

## Self-check
- [ ] Clean build has zero warnings with the chosen set.
- [ ] CI uses `-Werror`, local builds do not.

## Checked

2026-11-02. Confirmed against the GHC User's Guide using-warnings page: warning group contents, -Werror/-Wwarn forms, -Wunused-packages, -Wmissing-home-modules, -Wmisplaced-pragmas. Removed or fixed: -Wmissing-safe-haskell-mode and the --show-options hint; clarified -Wunused-packages.
Method: documentation only; no commands were run.
