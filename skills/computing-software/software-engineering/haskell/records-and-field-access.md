---
id: computing-software.software-engineering.haskell.records-and-field-access
name: records-and-field-access
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, records, record-syntax, field-selectors, record-update, namedfieldpuns, recordwildcards, overloadedrecorddot, records-and-field-access]
level: intro
status: docs-checked
description: "Define record types, use field selectors, update syntax, NamedFieldPuns, RecordWildCards and OverloadedRecordDot, and cope with duplicate field names."
sources: ["https://www.haskell.org/onlinereport/haskell2010/haskellch3.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/record_wildcards.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/overloaded_record_dot.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/field_selectors.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/using-warnings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Records

**Goal:** use records ergonomically and avoid the field-name clash problem.

```haskell
data Config = Config { host :: String, port :: Int } deriving (Show, Eq)
c = Config { host = "localhost", port = 8080 }
c' = c { port = 9090 }                 -- update: builds a new value
host c                                  -- selector function: Config -> String
```

## Extensions
```haskell
{-# LANGUAGE RecordWildCards, OverloadedRecordDot, DuplicateRecordFields #-}
g Config{..}         = host ++ show port        -- RecordWildCards: binds all fields
h c                  = c.host                   -- OverloadedRecordDot (GHC 9.2 and later)
mk host port = Config{..}                       -- wildcard construction from local names
```
Record puns (`Config{host, port}`) are a related extension; see the GHC User's Guide section on record puns.

## Rules
- Fields are top-level functions, so two records in one module cannot share a field name unless
  DuplicateRecordFields is on; `OverloadedRecordDot` (`c.host`) then picks the field by the record's type.
- Record update on a multi-constructor type gives bottom (a run-time error) if the value's constructor lacks the field.
- Construction with missing fields compiles with a warning (`-Wmissing-fields`, on by default) and the missing fields are
  bottom; omitting a strict field (`!Int`) is a compile-time error.
- Wildcards cannot be used in a record update, nor for constructors declared without record fields.
- Nested update is verbose; optics libraries are one answer.

## Gotchas
- RecordWildCards can hide where a name comes from; avoid in large scopes. In construction, `{..}` fills only fields whose names are bound locally (not imported or top-level).
- Partial field selectors: `-Wpartial-fields` flags a field defined in some but not all constructors.
- Prefixing fields (`cfgHost`) is the usual Haskell 2010 workaround.

## Self-check
- [ ] `-Wall -Wpartial-fields` clean.
- [ ] No two records share a bare field name unless DuplicateRecordFields and dot syntax are on.

## Checked

2026-11-08. Confirmed against the Haskell 2010 Report section 3.15 (record construction, strict fields, update on wrong constructor) and the GHC User's Guide: RecordWildCards (patterns, construction, restrictions), OverloadedRecordDot (since 9.2.0), field selectors and DuplicateRecordFields, `-Wmissing-fields` (on by default) and `-Wpartial-fields`. Removed: the NamedFieldPuns pragma and example (no puns page was read; only a pointer remains) and the sentence on type annotations.
Method: documentation only; no commands were run.
