---
id: computing-software.software-engineering.haskell.io-monad-and-main
name: io-monad-and-main
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, io-monad, main, putstrln, getline, interact, io-actions, unsafeperformio, io-monad-and-main, haskell-io]
level: intro
status: docs-checked
description: "Write main and IO actions: putStrLn, getLine, interact, getArgs, exit codes, buffering, and why IO values are descriptions that run only from main."
sources: ["https://www.haskell.org/onlinereport/haskell2010/", "https://hackage.haskell.org/package/base"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The IO monad and main

**Goal:** structure programs as a thin IO shell around pure functions.

```haskell
import System.Environment (getArgs, getProgName, lookupEnv)
import System.Exit
import System.IO

main :: IO ()
main = do
  hSetBuffering stdout LineBuffering
  args <- getArgs
  name <- maybe "world" id <$> lookupEnv "USER"
  putStrLn ("hello " ++ name)
  line <- getLine
  hPutStrLn stderr ("got " ++ line)
  if null args then exitWith (ExitFailure 2) else exitSuccess
```

## Rules
- An `IO a` value is an action description; evaluating it does nothing, running it from `main` does.
- `interact f` passes all of stdin to `f :: String -> String` and prints the result. Handy for filters.
- `getContents` is lazy IO; `readFile` is lazy too and keeps the file open until fully read.
- `exitWith` throws `ExitCode` as an exception; it can be caught by overly broad handlers.
- Pure code stays pure: `let` for pure values, `<-` only for IO results. `return` wraps, it does not unwrap.

## Gotchas
- Files are normally block-buffered and terminals line-buffered (the default is implementation-dependent), so prompts may not appear when output is redirected: use `hSetBuffering stdout NoBuffering` or `hFlush stdout`.
- `hSetEncoding stdout utf8` sets the text encoding of a handle.

## Self-check
- [ ] `echo hi | ./prog` and an interactive run behave the same (buffering).
- [ ] Non-ASCII output tested; `hSetEncoding` set where the default encoding is wrong.

## Checked

2026-11-03. Confirmed against base System.IO, System.Exit and System.Environment pages: buffering defaults, hFlush, hSetEncoding, exit codes. Removed: unsafePerformIO, main-type and locale error-message claims.
Method: documentation only; no commands were run.
