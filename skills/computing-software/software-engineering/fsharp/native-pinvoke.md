---
id: computing-software.software-engineering.fsharp.native-pinvoke
name: native-pinvoke
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, native-pinvoke, fsharp-interop, platform-invoke, dllimport]
level: advanced
status: draft
description: "Call native libraries from F# with DllImport, marshalling attributes and byref parameters."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# P/Invoke
**Goal:** call native functions safely.

```fsharp
open System.Runtime.InteropServices

module Native =
    [<DllImport("libc", EntryPoint = "getpid")>]
    extern int getpid()

    [<DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)>]
    extern bool SetConsoleTitle(string title)

    [<DllImport("mylib")>]
    extern int fill([<Out>] byte[] buf, int len)

let pid = Native.getpid ()
```
- Declare externs with `extern` and C-style signatures (`extern int f(int x)`).
- Pass pointers with `nativeint`, `byref`, `NativePtr`, or arrays; `[<MarshalAs>]` for strings and structs.
- Struct layouts need `[<StructLayout(LayoutKind.Sequential)>]` with `[<Struct>]`.
- Prefer `LibraryImport` source-generated P/Invoke only if available in F# (unconfirmed; F# does not run C# source generators).

## Gotchas
- Library names and calling conventions differ per OS; use `NativeLibrary` or conditional resolution for cross-platform.
- Mismatched signatures crash the process, not throw.

## Self-check
Call `getpid` and compare with `Environment.ProcessId`.
