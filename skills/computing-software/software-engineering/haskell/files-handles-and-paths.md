---
id: computing-software.software-engineering.haskell.files-handles-and-paths
name: files-handles-and-paths
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, readfile, writefile, withfile, hgetline, handle, filepath, directory, bracket, files-handles-and-paths]
level: practitioner
status: docs-checked
description: "Read and write files with readFile, withFile and Handles, use the filepath and directory packages, and avoid lazy-IO file handle leaks."
sources: ["https://www.haskell.org/onlinereport/haskell2010/", "https://hackage.haskell.org/package/base"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Files, handles and paths

**Goal:** do file IO safely, with resources released.

```haskell
import System.IO
import System.FilePath ((</>), takeExtension, takeFileName)   -- package filepath
import System.Directory (doesFileExist, listDirectory, createDirectoryIfMissing, removeFile)  -- package directory
import qualified Data.Text.IO as TIO

main = do
  withFile "out.txt" WriteMode $ \h -> do        -- closes the handle even on exceptions
    hPutStrLn h "line"
  s <- readFile "out.txt"
  length s `seq` pure ()                          -- force before reuse: readFile is lazy
  ex <- doesFileExist ("dir" </> "a.txt")
  txt <- TIO.readFile "data.txt"                  -- Data.Text.IO obeys the locale encoding
  appendFile "log.txt" "more\n"
```

## Rules
- Modes: `ReadMode`, `WriteMode` (truncates), `AppendMode`, `ReadWriteMode`.
- `hGetLine`, `hGetContents`, `hIsEOF`, `hClose`, `hSeek`, `hSetBinaryMode`, `openBinaryFile`.
- `bracket (openFile p ReadMode) hClose action` is the long form of `withFile`.
- Paths are `String` (`FilePath`).

## Gotchas
- `readFile` holds a semi-closed handle until the whole contents are consumed, so writing to that file (for example with `writeFile`) usually fails with `isAlreadyInUseError`. Read strictly (Text/ByteString) first.
- Use `openBinaryFile` or ByteString for binary data.
- `</>` with an absolute right side discards the left side.
- Atomic writes: write a temp file in the same directory and `renameFile`.

## Self-check
- [ ] No lazy `readFile` result outlives its use.
- [ ] Binary files read with `Data.ByteString`.

## Checked

2026-11-03. Confirmed against base System.IO and the filepath and directory pages: file modes, withFile, semi-closed readFile handle, renameFile, binary handles. Removed: os-string/file-io note, hGetContents truncation and newline-translation claims.
Method: documentation only; no commands were run.
