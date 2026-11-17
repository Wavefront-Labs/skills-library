---
id: computing-software.software-engineering.haskell.conduit-and-streaming-io
name: conduit-and-streaming-io
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, conduit, streaming, pipes, streamly, runconduit, resourcet, lazy-io-alternative, bracket-resource, conduit-and-streaming-io, haskell-streaming]
level: advanced
status: docs-checked
description: "Process large data in constant memory with conduit (sourceFile, .|, Data.Conduit.Combinators, sinkFile, runConduitRes with ResourceT) and know the alternative streaming packages."
sources: ["https://hackage.haskell.org/package/conduit", "https://hackage.haskell.org/package/conduit/docs/Data-Conduit.html", "https://hackage.haskell.org/package/conduit/docs/Data-Conduit-Combinators.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming I/O

**Goal:** replace lazy IO with resource-safe, constant-memory pipelines.

```haskell
import Conduit            -- package conduit (re-exports Data.Conduit and common combinators)
import qualified Data.Conduit.Combinators as C
import qualified Data.ByteString.Char8 as B

main = runConduitRes $                             -- ResourceT ensures files close on exceptions
     sourceFile "in.txt"                           -- Source: ByteString chunks
  .| C.linesUnboundedAscii                         -- Conduit: lines
  .| C.filter (not . B.null)
  .| C.map (B.map toUpper)
  .| C.unlines
  .| sinkFile "out.txt"                            -- Sink

count = runConduit $ yieldMany [1..1000000 :: Int] .| C.sum   -- constant memory
```
`.|` connects stages: `ConduitT i o m r` has input type `i`, output type `o`, base monad `m` and result `r`. Also exported: `awaitForever`, `yield`, `leftover`, `bracketP`, `sinkList`, `zipSources`.

## Alternatives
- Other Hackage streaming packages: `pipes-safe`, `streamly`, `io-streams` (compare their package pages and versions before choosing).
- `resourcet` provides `ResourceT`, which conduit depends on.

## Rules
- conduit's stated purpose is production, transformation and consumption of streams of data in constant memory.
- `runConduitRes` runs the pipeline inside `ResourceT`, which is how `sourceFile`/`sinkFile` handles are released.
- Use `Data.Conduit.Combinators` (`sourceFile`, `linesUnboundedAscii`, `sinkFile`) instead of `getContents`.
- Accumulating in a sink such as `sinkList` holds the whole result in memory; prefer a fold or `C.sum`-style consumer.

## Gotchas
- Chunk boundaries split lines; use the line combinators (`linesUnboundedAscii`) rather than splitting chunks yourself.
- `ResourceT` regions must enclose the whole pipeline.
- Mixing lazy IO and streaming loses the constant-memory guarantee.

## Self-check
- [ ] A multi-GB file processes with flat memory.
- [ ] Files close when an exception is thrown mid-stream.

## Checked
2026-11-03. Confirmed against the conduit package page and the Haddock pages for `Data.Conduit` (`runConduit`, `runConduitRes`, `.|`, `ConduitT`, `awaitForever`, `yield`, `leftover`, `bracketP`, `zipSources`) and `Data.Conduit.Combinators` (`sourceFile`, `sinkFile`, `linesUnboundedAscii`, `filter`, `map`, `unlines`, `yieldMany`, `sum`, `sinkList`). Removed: pull-based claim, `Data.Conduit.Binary`, `decodeUtf8C`, `http-conduit`/`conduit-extra` scope, `mapM_C`, `pipes`/`streaming`/`unliftio` descriptions, the streamly version note and `+RTS -s` advice.
Method: documentation only; no commands were run.
