---
id: computing-software.software-engineering.haskell.safe-haskell-and-unsafe-functions
name: safe-haskell-and-unsafe-functions
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, safe-haskell, trustworthy, unsafe, unsafeperformio, unsafecoerce, -xsafe, sandbox, plugins, safe-haskell-and-unsafe-functions, haskell-security]
level: sme
status: docs-checked
description: "Understand Safe Haskell modes (Safe, Trustworthy, Unsafe), -XSafe for untrusted code, and audit uses of unsafePerformIO, unsafeCoerce and FFI."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/safe_haskell.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe Haskell and unsafe functions

**Goal:** limit what untrusted or hard-to-review code can do and audit escape hatches.

## Safe Haskell
- `{-# LANGUAGE Safe #-}`: module may import only Safe or Trustworthy modules and uses a restricted language subset: `TemplateHaskell` is disabled; foreign imports must have IO types; RULES defined in the module are dropped; use of overlapping instances is restricted.
- `Trustworthy`: author asserts the module is safe even though it uses unsafe imports (the package maintainer vouches); `Unsafe`: explicitly unsafe.
- Compile flags: `-fpackage-trust`, `-trust pkg`, `-distrust-all-packages`. `ghc -Wunsafe -Wsafe -Wtrustworthy-safe`.
- Use case: running user plugins or scripts (the `hint` package interpreter with Safe flag) so they cannot call `unsafePerformIO` or `System.IO`.
- It is a type-level guarantee, not a sandbox for CPU/memory: combine with OS isolation and `timeout`.

## Audit list (grep)
```bash
grep -rnE "unsafePerformIO|unsafeCoerce|unsafeDupablePerformIO|inlinePerformIO|unsafeInterleaveIO|unsafeIndex|unsafeRead|unsafeFreeze|Foreign\.|foreign import" src
```
Each hit needs a comment explaining the invariant. Also `Data.ByteString.Unsafe`, `GHC.Exts` primops, `Debug.Trace`, `error`/`undefined`.

## Gotchas
- Safe Haskell is little used in practice; most libraries are `Trustworthy` or `Unsafe` so a Safe module may not be able to import much.
- Template Haskell and plugins run arbitrary code at compile time: reviewing dependencies matters.
- `-XSafe` does not prevent infinite loops or memory exhaustion.

## Self-check
- [ ] Every unsafe call has a justification comment and a test.
- [ ] Untrusted code runs in a separate process with resource limits as well.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/safe_haskell and using-warnings pages: disabled and restricted features, -fpackage-trust, -Wunsafe, -Wsafe. Removed or fixed: wrong restriction list.
Method: documentation only; no commands were run.
