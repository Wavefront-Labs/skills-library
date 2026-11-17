---
id: computing-software.software-engineering.haskell.string-vs-text
name: string-vs-text
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, string, text, data-text, pack, unpack, text-io, utf8, char, string-vs-text, haskell-text]
level: intro
status: docs-checked
description: "Decide between String and Data.Text, convert with pack/unpack, use the T and TIO imports, and avoid locale-dependent IO."
sources: ["https://hackage.haskell.org/package//text"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String vs Text

**Goal:** use Text for real text processing; keep String for small, interop-driven cases.

```haskell
import qualified Data.Text as T
import qualified Data.Text.IO as TIO
import qualified Data.Text.Encoding as TE

t = T.pack "héllo"              -- String to Text
s = T.unpack t
TIO.putStrLn (T.toUpper t)
T.length t                       -- O(n), counts code points
T.words "a b  c"; T.splitOn "," "a,b,c"; T.strip " x "; T.intercalate ", " ["a","b"]
T.replace "a" "b" "banana"; T.isPrefixOf; T.breakOn "=" "k=v"
TE.encodeUtf8 t                  -- Text to strict ByteString
TE.decodeUtf8' bytes             -- Either UnicodeException Text (safe); decodeUtf8 throws
```

## Facts
- `Text` (`Data.Text`) is an immutable Unicode string type with list-like functions (`T.words`, `T.splitOn`, `T.replace`, `T.breakOn`).
- `Data.Text.Read` (`decimal`, `signed`, `double`) parses numbers from `Text`.
- `Data.Text.Lazy.Builder` provides a Builder for assembling text.

## Gotchas
- `T.length` is O(n) and counts characters (code points), not graphemes: an accented letter can be one code point or two. The docs point to the `text-icu` package for richer Unicode and locale operations.
- `T.toUpper` uses simple case conversion and is not locale sensitive.
- `TIO.readFile` obeys the runtime system's locale encoding and is slow; for UTF-8 data the docs suggest `decodeUtf8 . readFile` with ByteString's `readFile`.

## Self-check
- [ ] `decodeUtf8'` used for untrusted bytes.

## Checked

2026-11-03. Confirmed against the text Data.Text, Data.Text.IO, Data.Text.Encoding and Data.Text.Read pages: length O(n), toUpper simple case conversion, text-icu pointer, locale-dependent IO, Read functions. Removed: UTF-8 internals and String size claims, show-escaping claim. Fixed toUpper description.
Method: documentation only; no commands were run.
