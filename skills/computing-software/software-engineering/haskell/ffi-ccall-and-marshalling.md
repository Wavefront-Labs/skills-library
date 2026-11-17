---
id: computing-software.software-engineering.haskell.ffi-ccall-and-marshalling
name: ffi-ccall-and-marshalling
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, ffi, foreign-import, ccall, foreign-ptr, storable, withcstring, alloca, capi, unsafe-safe, hsc2hs, ffi-ccall-and-marshalling, haskell-ffi]
level: advanced
status: docs-checked
description: "Call C from Haskell with foreign import ccall, marshal with Foreign.C.Types, Ptr, alloca, withCString and Storable, safe/unsafe calls and capi."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/ffi.html", "https://www.haskell.org/onlinereport/haskell2010/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FFI: calling C

**Goal:** bind a C function correctly and safely.

```haskell
{-# LANGUAGE ForeignFunctionInterface, CApiFFI #-}
import Foreign
import Foreign.C.Types
import Foreign.C.String

foreign import ccall unsafe "math.h sin"   c_sin :: CDouble -> CDouble
foreign import ccall safe   "mylib.h process" c_process :: Ptr CChar -> CInt -> IO CInt
foreign import capi  "stdlib.h value EXIT_FAILURE" exitFailureC :: CInt   -- constants/macros via capi

process :: String -> Int -> IO Int
process s n = withCString s $ \cs -> fromIntegral <$> c_process cs (fromIntegral n)

sumArr :: [CInt] -> IO CInt
sumArr xs = withArrayLen xs $ \len p -> c_sum p (fromIntegral len)
alloca $ \p -> do { poke p (5 :: CInt); c_inc p; peek p }
```

## Rules
- Use Foreign.C types (`CInt`, `CDouble`, `CSize`, `CChar`) at the boundary, not `Int`/`Double`, because C widths vary by platform.
- `unsafe` calls are fast but must not call back into Haskell and block the whole capability; `safe` calls (default) allow other Haskell threads to run and callbacks. `interruptible` (needs the `InterruptibleFFI` extension) lets the call be interrupted by `killThread`. `ccall` cannot call varargs C functions; use `capi` with an explicit signature.
- Marshal with `with`, `alloca`, `allocaBytes`, `withCString`, `withArray`, `newForeignPtr` (finalizers via `finalizerFree` or a C function).
- `Storable` instances define `sizeOf`, `alignment`, `peek`, `poke`; `hsc2hs` (`#{size}`, `#{peek}`) generates struct layouts from C headers.
- `foreign import ccall "wrapper"` makes a C function pointer from a Haskell function; free it with `freeHaskellFunPtr`.
- `foreign export ccall` exposes Haskell to C.
- Link libraries: cabal `extra-libraries: m`, `c-sources: cbits/foo.c`, `include-dirs`, `pkgconfig-depends: zlib`.

## Gotchas
- ForeignPtr finalizers run at GC time on an unspecified thread; do not rely on timing.
- Pointers into Haskell heap objects are invalid after GC unless pinned (`ByteString` buffers, `mallocForeignPtrBytes`).
- Calling convention mismatch on 32-bit Windows (`stdcall`).
- Wrong `IO` omission: a function with side effects typed pure may be duplicated or dropped.

## Self-check
- [ ] Every foreign import is typed IO unless truly pure.
- [ ] Struct layouts come from hsc2hs, not hand-computed offsets.

## Checked

2026-11-02. Confirmed against the GHC User's Guide exts/ffi page: capi, varargs, wrapper, InterruptibleFFI. Removed or fixed: interruptible without extension.
Method: documentation only; no commands were run.
