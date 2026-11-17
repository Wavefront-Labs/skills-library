---
id: computing-software.software-engineering.haskell.haskell-style-guides
name: haskell-style-guides
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, style-guide, tibell, kowainik, naming, haddock-conventions, import-conventions, api-design, haskell-style-guides]
level: practitioner
status: draft
description: "Apply common Haskell conventions: Johan Tibell and Kowainik style guides, naming, import style, error and partial function policy, Haddock and API design."
sources: ["https://github.com/ndmitchell/hlint", "https://github.com/tweag/ormolu", "https://github.com/fourmolu/fourmolu"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Haskell style guides

**Goal:** write code that matches community expectations. Sources: Johan Tibell's style guide, Kowainik's style guide, GHC's own commentary, and the formatter's output.

## Naming
- Modules `UpperCamel` with dots matching directories; types and constructors `UpperCamel`; functions and variables `lowerCamel`.
- Type variables: short (`a`, `b`, `m`, `f`), meaningful for phantom or domain types.
- Operators: avoid inventing new ones for one use; document fixity.
- Boolean functions: `isX`/`hasX`; conversions `toX`/`fromX`; unsafe variants prefixed or named `unsafeX`.

## Layout
- Indent 2 or 4 spaces consistently (let the formatter decide); line length around 80 to 100.
- Imports: qualified for containers/Text, explicit lists for others; one import per line; sorted.
- Top-level signatures always; local signatures for non-obvious helpers.

## API and safety
- Export lists on every module of a library; keep constructors abstract with smart constructors.
- Prefer total functions: `NonEmpty`, `Maybe`, `Either`; avoid `head`, `fromJust`, `error`.
- Records: strict fields for data; avoid positional constructors beyond 3 fields.
- Prefer newtypes over type synonyms for domain concepts.
- Avoid orphan instances; avoid `String` for text; avoid lazy IO.
- Default to `-Wall`; adopt `-Wcompat`, `-Widentities`, `-Wredundant-constraints`, `-Wmissing-export-lists` selectively.
- Haddock: document every export, with an example where useful.

## Gotchas
- Style guides disagree (leading vs trailing commas); one rule wins: follow the project's formatter config.
- "Avoid success at all costs": do not imitate clever type-level code in application layers unless the team knows it.
- Keep module dependencies acyclic and layered (types, pure core, IO shell).

## Self-check
- [ ] A new contributor can reproduce formatting with a single command.
- [ ] Public API reviewed for partial functions and abstractions.
