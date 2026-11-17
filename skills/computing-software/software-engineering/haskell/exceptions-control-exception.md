---
id: computing-software.software-engineering.haskell.exceptions-control-exception
name: exceptions-control-exception
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, exceptions, throwio, catch, try, bracket, finally, evaluate, asyncexception, someexception, custom-exception, exceptions-control-exception]
level: advanced
status: docs-checked
description: "Throw and catch synchronous exceptions with throwIO, try, catch, bracket and finally, define exception types, and handle async exceptions and evaluate correctly."
sources: ["https://hackage.haskell.org/package/base"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exceptions in IO

**Goal:** handle runtime failures and clean up resources correctly. Module: `Control.Exception`.

```haskell
{-# LANGUAGE ScopedTypeVariables #-}
import Control.Exception

data AppErr = AppErr String deriving Show
instance Exception AppErr                 -- default methods suffice

main = do
  r <- try (readFile "nope") :: IO (Either IOException String)   -- type picks which exception
  case r of Left e -> putStrLn ("failed: " ++ show e); Right _ -> pure ()
  handle (\(e :: ArithException) -> print e) (print (1 `div` (0 :: Int)))
  throwIO (AppErr "boom") `catch` \(AppErr m) -> putStrLn m
  r2 <- try (evaluate (head [])) :: IO (Either SomeException Int)   -- evaluate forces inside try
  withResource `finally` putStrLn "cleanup"
  bracket acquire release use          -- release runs even on exception
```

## Rules
- `throwIO` for IO; `throw` for pure code (raised when forced). Prefer `throwIO`.
- `try`'s exception type must be determinable; `SomeException` catches everything.
- `bracket_`, `bracketOnError`, `onException`, `mask` for resource control.
- `evaluate x` forces to weak head normal form inside the IO action, uncovering exceptions a lazy value may contain.
- Exception hierarchies use `toException`/`fromException`; `ExitCode`, `AsyncException` (`UserInterrupt`, `StackOverflow`) and `SomeAsyncException` are separate types.

## Gotchas
- `catch` runs its handler inside an implicit mask and `try` does not; the docs recommend `try` for ordinary recovery and `catch` or `catchJust` when recovering from asynchronous exceptions.
- Lazy values can hide exceptions; `evaluate` uncovers them, and `force` from `Control.DeepSeq` evaluates deeper than WHNF.
- `evaluate x` and `return $! x` differ: if `x` throws, `return $! x` throws while the action is built, `evaluate x` when it is run.

## Self-check
- [ ] No `SomeException` handler that swallows asynchronous exceptions such as `UserInterrupt`.
- [ ] Resources acquired via `bracket`/`withFile`, never manual open/close.

## Checked

2026-11-03. Confirmed against the base Control.Exception page: throw/throwIO, evaluate to WHNF and its difference from return $!, bracket_, onException, SomeAsyncException, try vs catch masking. Removed: safe-exceptions/unliftio advice, undefined callstack claim, System.IO.Error example.
Method: documentation only; no commands were run.
