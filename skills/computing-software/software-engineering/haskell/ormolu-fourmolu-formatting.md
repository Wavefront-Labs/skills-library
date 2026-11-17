---
id: computing-software.software-engineering.haskell.ormolu-fourmolu-formatting
name: ormolu-fourmolu-formatting
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, ormolu, fourmolu, stylish-haskell, code-formatter, fourmolu-yaml, format-on-save, brittany, ormolu-fourmolu-formatting, haskell-lintfmt]
level: intro
status: docs-checked
description: "Format Haskell with Ormolu or Fourmolu (fourmolu.yaml): inplace and check modes for CI, cabal default-extensions, -o flags, CPP limits and exit codes."
sources: ["https://github.com/tweag/ormolu", "https://github.com/fourmolu/fourmolu", "https://fourmolu.github.io/config/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ormolu and Fourmolu

**Goal:** one automatic style, never argued in review.

```bash
cabal install ormolu; cabal install fourmolu
ormolu --mode inplace $(git ls-files '*.hs')
ormolu --mode check   $(git ls-files '*.hs')             # CI: exit non-zero if changes needed
fourmolu -i src                                          # same as --mode inplace
fourmolu --mode check src                                # CI check
fourmolu --print-defaults > fourmolu.yaml                # config with default values
```

## Fourmolu config (`fourmolu.yaml`)
```yaml
indentation: 2
column-limit: none
function-arrows: trailing
comma-style: trailing
import-export-style: trailing
newlines-between-decls: 1
respectful: false
```
These are the values of Fourmolu's own `fourmolu.yaml`, which imitates Ormolu's style. Fourmolu looks for `fourmolu.yaml` in all parents of the current directory; every option can also be given on the command line (`--indentation 2`). Other options on the config page include `record-style`, `import-grouping`, `indent-wheres`, `let-style`, `if-style`, `haddock-style`, `unicode`, `fixities` and `reexports`. Ormolu has no style options.

## Rules
- Both locate the `.cabal` file for a source file and take default extensions and dependencies (used for operator fixities) from it; `--no-cabal` disables that. Ormolu also reads `.ormolu` files for fixity overrides (`--no-dot-ormolu` disables it).
- Extra language extensions: pass `-o` or `--ghc-opt` (for example `-o -XLambdaCase`).
- Output always uses LF line endings, so `--mode check` fails on CRLF input that is otherwise formatted.
- CPP support is experimental: CPP sections are treated as unchangeable snippets, which works only in simple cases.
- Haskell Language Server has built-in support for using Ormolu as a formatter.
- Use the same formatter version in CI and in editors, since output can change between versions.

## Gotchas
- A parse error means formatting is skipped; fix the code first.
- `--mode inplace` does not work with stdin input (exit code 101); stdin input with `.cabal` lookup needs a file path (exit code 9).
- Keep the CI `--mode check` as the source of truth for style.

## Self-check
- [ ] `--mode check` passes locally and in CI with the same formatter version.
- [ ] Config file committed.

## Checked
2026-11-03. Confirmed against the Ormolu and Fourmolu READMEs and the Fourmolu configuration page and default `fourmolu.yaml`: install via cabal, `--mode inplace`/`check`, `-i`, `--print-defaults`, cabal and `.ormolu` lookup with `--no-cabal`/`--no-dot-ormolu`, `-o`/`--ghc-opt`, LF output, CPP limits, exit codes 9 and 101, HLS Ormolu support, option names and default values. Removed: `fourmolu --help` advice, `function-arrows: leading`, `comma-style: leading`, `in-class-decls`, `haddock-style: single-line`, pre-commit hooks, `.tool-versions`, stylish-haskell and brittany remarks.
Method: documentation only; no commands were run.
