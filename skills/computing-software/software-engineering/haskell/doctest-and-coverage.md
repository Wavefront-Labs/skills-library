---
id: computing-software.software-engineering.haskell.doctest-and-coverage
name: doctest-and-coverage
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, doctest, hpc, coverage, hpc-markup, cabal-doctest, haddock-examples, test-coverage, doctest-and-coverage]
level: practitioner
status: docs-checked
description: "Verify Haddock examples with doctest (cabal repl --with-compiler=doctest) and enable HPC coverage with cabal --enable-coverage or stack test --coverage."
sources: ["https://hackage.haskell.org/package/doctest", "https://cabal.readthedocs.io/en/stable/cabal-project-description-file.html", "https://docs.haskellstack.org/en/stable/commands/hpc_command/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# doctest and HPC coverage

**Goal:** keep documentation examples honest and see what tests exercise.

## doctest
```haskell
-- | Add one.
--
-- >>> inc 41
-- 42
-- >>> map inc [1,2]
-- [2,3]
inc :: Int -> Int
inc = (+ 1)
```
```bash
cabal install doctest --ignore-project --overwrite-policy=always
cabal build
cabal repl --with-compiler=doctest       # the doctest package's recommended way for a Cabal package
doctest src/Fib.hs                       # a single file, without Cabal
```
A comment line starting with `>>>` is an expression; the comment lines after it are the expected result, defined by what a REPL (ghci) prints to stdout and stderr. Doctest options can be passed to `cabal repl` with `--repl-options`; properties need `--build-depends=QuickCheck` and `--build-depends=template-haskell`.

## HPC (Haskell Program Coverage)
```bash
cabal test --enable-coverage          # libraries and executables (including test suites) built with HPC; running the tests generates coverage reports
stack test --coverage                 # the Stack equivalent
```
Cabal's `coverage` setting (`--enable-coverage` / `--disable-coverage`, since Cabal 1.22) builds with Haskell Program Coverage enabled. Stack passes `-fhpc` to all project packages, which makes executables record coverage to `.tix` files; `stack hpc report` combines `.tix` files into a report.

## Gotchas
- Stack deletes an existing `<test-name>.tix` file before a test run; `.tix` files from executables are not considered by `stack hpc report` unless listed by name.
- Coverage does not equal correctness; combine with properties.
- doctest evaluates examples in a REPL, so output must match exactly what the REPL prints.

## Self-check
- [ ] All doc examples pass in CI.
- [ ] Coverage trend tracked, not just a gate number.

## Checked
2026-11-03. Confirmed against the doctest Hackage page (`>>>` syntax, `cabal repl --with-compiler=doctest`, install command, `--repl-options`, `--build-depends`), the Cabal project description (`--enable-coverage`) and the Stack hpc and build pages (`--coverage`, `-fhpc`, `.tix`, `stack hpc report`). Removed: `--with-ghc`, standalone `hpc report`/`hpc markup` commands and the coverage-kind list (the GHC HPC page was not reachable), cabal-docspec, multi-line `:{` syntax and extension advice (not on the doctest page).
Method: documentation only; no commands were run.
