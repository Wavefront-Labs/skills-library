---
id: computing-software.software-engineering.haskell.bytestring-strict-lazy-char8
name: bytestring-strict-lazy-char8
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, bytestring, bytestring-lazy, char8, packedchars, readfile-strict, hgetcontents, binary-data, bytestring-strict-lazy-char8, haskell-bytestring]
level: practitioner
status: docs-checked
description: "Use strict and lazy ByteString, the Char8 interface and its truncation hazard, UTF-8 interplay with Text, and IO functions."
sources: ["https://hackage.haskell.org/package//bytestring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ByteString

**Goal:** handle binary data and fast byte-oriented IO.

```haskell
import qualified Data.ByteString as B
import qualified Data.ByteString.Char8 as BC
import qualified Data.ByteString.Lazy as BL
import qualified Data.Text.Encoding as TE

bs <- B.readFile "data.bin"            -- strict: whole file in memory
B.length bs; B.take 4 bs; B.unpack (B.take 2 bs)   -- [Word8]
BC.pack "ascii only"; BC.lines; BC.words; BC.readInt "123 rest"   -- Maybe (Int, ByteString)
lazy <- BL.readFile "big.bin"          -- lazy: a lazy list of strict chunks
BL.toStrict lazy; BL.fromStrict bs
TE.decodeUtf8' bs                       -- bytes to Text
```

## Facts
- `Data.ByteString` strict: one contiguous pinned buffer; `Data.ByteString.Lazy`: list of strict chunks.
- `Char8` functions truncate every `Char` to 8 bits (bytes are taken as code points 0-255). Never use for non-ASCII text.
- `BC.readInt` reads a signed `Int` from the start of the input (leading whitespace is not skipped) and returns `Just (value, rest)`; `Nothing` if the value overflows `Int`.
- `Data.ByteString.Builder` assembles output efficiently (`toLazyByteString`, `intDec`, `byteString`, `hPutBuilder`).
- `ShortByteString` is backed by unpinned memory and avoids heap fragmentation; converting to or from `ByteString` copies.

## Gotchas
- `B.copy` makes a copy with its own storage so the rest of a large string can be garbage collected when only a small part is kept.
- Pinned memory can cause heap fragmentation if a program keeps a fraction of many small `ByteString`s alive for a long time.
- `fromString` (the `IsString` instance, used with `OverloadedStrings`) truncates multi-byte characters to octets.

## Self-check
- [ ] Text goes through UTF-8 encode/decode, never `Char8`.
- [ ] Large outputs use Builder.

## Checked

2026-11-03. Confirmed against the bytestring Data.ByteString, Char8, Lazy and Short pages: pinned memory, Char8 truncation, readInt behaviour, copy, ShortByteString, fromString truncation. Removed: show, lazy hGetContents and network-protocol advice.
Method: documentation only; no commands were run.
