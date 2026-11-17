---
id: computing-software.software-engineering.csharp-dotnet.unsafe-code-and-pointers
name: unsafe-code-and-pointers
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-interop, unsafe-pointers, unsafe-code, fixed-statement, stackalloc, fixed-size-buffers, function-pointers]
level: advanced
status: docs-checked
description: "Use unsafe C#, pointers, fixed, fixed-size buffers, function pointers and stackalloc only where needed: AllowUnsafeBlocks, pinning scope, stackalloc limits, best practices."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/unsafe-code", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/stackalloc", "https://learn.microsoft.com/en-us/dotnet/standard/unsafe-code/best-practices", "https://learn.microsoft.com/en-us/dotnet/core/compatibility/code-analysis/5.0/ca2014-stackalloc-in-loops"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unsafe code and pointers

Unsafe code is not necessarily dangerous, only unverifiable by .NET tools. Use it to call native functions that need pointers and, in some cases, for direct memory access that avoids array-bounds checks. Compiling an `unsafe` context needs the `AllowUnsafeBlocks` compiler option (`<AllowUnsafeBlocks>true</AllowUnsafeBlocks>`).

```csharp
unsafe static int Sum(int[] data)
{
    fixed (int* p = data)                 // pins the array: the GC will not move it inside the block
    {
        int s = 0;
        for (int i = 0; i < data.Length; i++) s += p[i];
        return s;
    }
}
Span<byte> buf = stackalloc byte[256];    // assigning to Span/ReadOnlySpan needs no unsafe context
```

## Pointer rules (original model, the default)
- Pointer features (pointer types, `&`, `*p`, `p->m`, `p[i]`, `fixed`, converting `stackalloc` to a pointer, `sizeof` on arbitrary types) need an `unsafe` context. Declare several pointers as `int* p1, p2;`, not `int *p1, *p2`.
- Pointer types do not derive from `object`; there is no boxing, but explicit conversions to integral types and other pointer types exist. `void*` cannot be dereferenced; cast first. Dereferencing a null pointer has implementation-defined behaviour.
- The GC does not track pointers. If the referent is on the managed heap you must pin it (`fixed`) for as long as the pointer is used.
- Returning or passing out a pointer set inside a `fixed` block can leave it pointing at a variable that is no longer fixed.
- Fixed-size buffers (`fixed char name[30];`): instance fields of structs only, length required, one-dimensional, element type limited to `bool`, `byte`, `char`, `short`, `int`, `long`, `sbyte`, `ushort`, `uint`, `ulong`, `float`, `double`, and only usable in an `unsafe` context.
- Function pointers (`delegate*`) call via `calli` instead of creating a delegate; only declarable and callable in an unsafe context, and `&` on a method works only for static methods.
- A preview "updated memory safety model" (C# 15 / .NET 11) narrows what needs `unsafe` and makes the modifier a caller contract; it is not the default.

## stackalloc
- Memory is discarded when the method returns and cannot be freed. Its contents are undefined (unlike `new`), so initialise or `Clear()` it.
- Prefer `Span<T>`/`ReadOnlySpan<T>` over pointers. `stackalloc T[E]` needs an unmanaged `T` and a non-negative `int` length.
- Too much stack throws `StackOverflowException`, which cannot be caught: cap the size and use an array above the cap, and never pass a negative or unbounded user-derived length.
- Do not use it in loops (CA2014, a default build warning since .NET 5); allocate once outside the loop.
- Stackalloc enables the CLR's buffer overrun detection, which terminates the process on a detected overrun.

## Best practices (Microsoft "Unsafe code best practices")
- Keep pointers inside the `fixed` scope: storing, returning or passing one so it escapes creates a dangling pointer. Prefer ref structs for built-in escape analysis.
- Do not use a pointer from `Unsafe.AsPointer` that can outlive the object; use `GCHandle` or `fixed` scopes to pin explicitly.
- Do not rely on `Unsafe.As` for struct-to-struct or class-to-class casts unless sure; prefer `Unsafe.BitCast`.
- Consume `stackalloc` into a `Span<T>` to keep bounds checks; for larger or escaping buffers use heap or unmanaged memory such as `NativeMemory.Alloc`.
- Do not assume no compiler warnings means correct code, and do not suppress warnings such as CS9123 (`&` on locals or parameters in async methods).
- Fuzz-test unsafe code (the page names SharpFuzz).

## Verify
Fuzz or property-test with edge lengths (0, 1, large and negative), and compare results with a safe `Span` version.

## Checked
2026-11-03. Confirmed against dotnet/docs: "Unsafe code, pointer types, and function pointers", the `stackalloc` reference, "Unsafe code best practices" and the CA2014 breaking-change page. Removed because not found there: the 1 KB stackalloc threshold, `NativeMemory`/`MemoryMarshal` API behaviour and `NativeMemory.Free` pairing (their API pages are not in dotnet/docs), `GC.AllocateArray(pinned: true)`, "pinning fragments the heap", `StructLayout` architecture remarks, Vector128/256 and ArrayPool advice, and the benchmark suggestion.
Method: documentation only; no commands were run.
