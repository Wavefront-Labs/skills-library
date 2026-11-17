---
id: computing-software.software-engineering.csharp-dotnet.libraryimport-pinvoke-and-marshalling
name: libraryimport-pinvoke-and-marshalling
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-interop, libraryimport-pinvoke, marshalling, dllimport, safehandle, native-interop]
level: advanced
status: docs-checked
description: "Call native libraries from C# with source-generated LibraryImport (.NET 7+) or DllImport: string, bool and struct marshalling, SafeHandle, callbacks and error codes."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/native-interop/pinvoke", "https://learn.microsoft.com/en-us/dotnet/standard/native-interop/pinvoke-source-generation", "https://learn.microsoft.com/en-us/dotnet/standard/native-interop/best-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LibraryImport, P/Invoke and marshalling

```csharp
internal static partial class Native
{
    [LibraryImport("user32.dll", StringMarshalling = StringMarshalling.Utf16, SetLastError = true)]
    internal static partial int MessageBoxW(IntPtr hWnd, string lpText, string lpCaption, uint uType);

    [LibraryImport("libc.so.6")]
    internal static partial int getpid();                   // macOS uses "libSystem.dylib"
}
// after a SetLastError = true call: int err = Marshal.GetLastPInvokeError();
```
.NET 7 introduced a source generator that finds `[LibraryImport]` on a `static partial` method and generates the marshalling code at compile time, removing the runtime IL stub and allowing the P/Invoke to be inlined. It needs `AllowUnsafeBlocks`. Microsoft's guidance: use `[LibraryImport]` when targeting .NET 7+; analyzer SYSLIB1054 tells you when `[DllImport]` is still appropriate.

## Migrating from DllImport
- `CallingConvention` has no equivalent; use `[UnmanagedCallConv(CallConvs = new[] { typeof(CallConvStdcall) })]`.
- `CharSet` is replaced by `StringMarshalling` (ANSI removed, UTF-8 is first-class). Some `MarshalAs` settings are unsupported and the generator reports an error.
- `LibraryImport` generally needs explicit settings rather than defaults.

## Marshalling rules (from the best-practices page)
- Match the native signature and use the closest .NET type (`uint` for unsigned int); prefer structs over classes for native types.
- Blittable types (primitives, `nint`, pointers, fixed-layout structs of blittable fields) are pinned instead of copied. `bool` is not blittable: by default it marshals as the 4-byte Windows `BOOL`, while C/C++ `bool` is one byte, which causes hard-to-track bugs; use `[MarshalAs]` deliberately.
- Strings passed by value are pinned and used directly when `StringMarshalling` is `Utf16`, the argument is `LPWSTR`, or `CharSet` is Unicode. Do not use `[Out] string` (it can destabilise the runtime for interned strings); prefer a pooled `char[]` or `byte[]` the native code fills. Avoid `StringBuilder` parameters: each call makes several copies and allocations.
- Use `SafeHandle` to manage lifetime of unmanaged resources; avoid finalizers for this.
- Callbacks: prefer function pointers with `UnmanagedCallersOnly` over delegate types.
- `SetLastError = true`: read the error before making other calls so it is not overwritten.
- Keep managed objects alive across native calls with `SafeHandle` (replaces `HandleRef`), `GC.KeepAlive`, or a `GCHandle` that you free explicitly.
- Library names differ per OS (`libc.so.6`, `libSystem.dylib`, `user32.dll`).

## Checked
2026-11-08. Confirmed against the Platform Invoke page (LibraryImport samples, Windows, macOS and Linux library names, SetLastError and GetLastPInvokeError), the P/Invoke source generation page (.NET 7, partial/static, AllowUnsafeBlocks, UnmanagedCallConv, differences from DllImport) and the native interop best-practices page (rules above). Removed as unconfirmed: the CreateFile/SafeFileHandle sample, wchar_t size remark, struct Pack advice, NativeMemory/FreeCoTaskMem allocator advice, NativeLibrary.SetDllImportResolver, "SYSLIB1050 series" and the CI verification step.
Method: documentation only; no commands were run.
