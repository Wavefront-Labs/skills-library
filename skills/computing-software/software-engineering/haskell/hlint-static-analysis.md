---
id: computing-software.software-engineering.haskell.hlint-static-analysis
name: hlint-static-analysis
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, hlint, hlint-yaml, ignore, suggestions, refactor, apply-refact, static-analysis, warning-vs-error, hlint-static-analysis]
level: practitioner
status: docs-checked
description: "Run HLint, generate .hlint.yaml, configure ignore, warn, error and custom rules, restrict functions and modules, use inline ignores and apply-refact."
sources: ["https://github.com/ndmitchell/hlint"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HLint

**Goal:** catch redundant code, partial functions and style issues automatically.

```bash
cabal install hlint
hlint src app test                   # prints suggestions with line numbers
hlint src --refactor --refactor-options="-i"    # apply via apply-refact
hlint --default > .hlint.yaml        # generate a starting config
hlint src --report                   # HTML report
```

## .hlint.yaml
```yaml
- ignore: {name: Eta reduce, within: [MyModule1, MyModule2]}
- error:  {name: Use concatMap}                  # warn or suggest also work
- warn:   {lhs: concat (map f x), rhs: concatMap f x}   # custom rule
- group: {name: future, enabled: true}      # enable a hint group
- arguments: [-XArrows]                     # extension flags
- modules:
  - {name: [Data.Set, Data.HashSet], as: Set, asRequired: true}   # enforce import alias
- functions:
  - {name: nub, within: []}                 # ban a function everywhere
```
Inline: `{-# HLINT ignore "Eta reduce" #-}` (also `{- HLINT ignore -}` and `{-# ANN module "HLint: ignore" #-}`) ignores a hint for the module; `{-# HLINT ignore myDef #-}` ignores hints in one definition.

## Rules
- Hints have severities: suggestion, warning, error. Only `.hlint.yaml` is picked up automatically (from the current directory or a parent); any other file name needs `--hint=FILE`.
- HLint is syntactic: it can suggest changes that alter strictness or typeclass defaulting. Read before applying.
- Custom rules are patterns with `lhs`/`rhs`.

## Gotchas
- HLint enables most extensions but disables ones that steal syntax (Arrows, TransformListComp, TypeApplications); enable them with `-XArrows` style flags in `arguments`.
- Large codebases: `-j4` runs on 4 processors (`-j` alone uses the number of physical processors).
- Start an existing project with `hlint . --report`, then `hlint . --default > .hlint.yaml`, which ignores every hint currently outstanding.

## Self-check
- [ ] `hlint .` is clean or only intentional ignores remain.
- [ ] Every ignore has a reason in a comment.

## Checked
2026-11-03. Confirmed against the HLint README: commands (`--refactor`, `--refactor-options` with `-i`, `--default`, `--report`, `-j`, `--hint=FILE`), `.hlint.yaml` lookup, ignore/warn/error with `name`, `within` and `lhs`/`rhs`, `group`, `arguments`, `modules` (`as`, `asRequired`), `functions` with `within: []`, inline HLINT/ANN pragmas, extension handling. Removed: the camelCase hint, `-XGHC2021`, cabal default-extensions, `--threads`, the claim that HLS runs HLint as a plugin.
Method: documentation only; no commands were run.
