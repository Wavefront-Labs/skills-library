---
id: computing-software.software-engineering.haskell.regex-and-text-search
name: regex-and-text-search
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, regex, regex-tdfa, pcre2, text-icu, replace-megaparsec, regex-applicative, string-search, regex-and-text-search]
level: practitioner
status: draft
description: "Match text with regex-tdfa or PCRE bindings, regex-applicative and megaparsec-based replacements, and know the performance and Unicode caveats."
sources: ["https://hackage.haskell.org/package//aeson", "https://hackage.haskell.org/package//megaparsec", "https://hackage.haskell.org/package//attoparsec"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regex and text search

**Goal:** pick a matching tool and use it safely.

```haskell
import Text.Regex.TDFA              -- package regex-tdfa (POSIX ERE, pure Haskell)

"2026-11-02" =~ ("([0-9]{4})-([0-9]{2})" :: String) :: (String, String, String, [String])   -- (before, match, after, groups)
("abc" =~ ("b" :: String)) :: Bool
getAllTextMatches ("a1b22" =~ ("[0-9]+" :: String)) :: [String]
```
The `=~` return type chooses the result (Bool, String, tuple, `AllMatches`, `MatchArray`).

## Options
- `regex-tdfa`: pure, POSIX leftmost-longest semantics, supports String/Text/ByteString; can be slower than PCRE on big inputs.
- `pcre-light`, `regex-pcre`, `pcre2` (binding to libpcre): Perl syntax and speed, requires the C library.
- `regex-applicative`: build regexes with Applicative combinators and semantic actions (type-safe extraction).
- `replace-megaparsec` / `replace-attoparsec`: find-and-replace with parsers (`streamEdit`).
- Plain text search: `T.isInfixOf`, `T.breakOn`, `T.splitOn`; `Data.ByteString.Search` (`stringsearch`) for substring search.
- `text-icu` for Unicode-aware regexes, collation and normalisation (links ICU).

## Gotchas
- User-supplied patterns can cause catastrophic backtracking in PCRE; TDFA is automaton based (safer) but memory can grow. Apply input limits.
- `=~` with String literals needs annotations when OverloadedStrings is on.
- Anchors and multiline flags differ between engines; check docs for `^`/`$` semantics.
- Regex is a poor fit for nested structures; use a parser.

## Self-check
- [ ] Untrusted patterns are length-limited or avoided.
- [ ] Tests cover Unicode input if relevant.
