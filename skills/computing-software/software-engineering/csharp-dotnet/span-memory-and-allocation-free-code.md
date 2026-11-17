---
id: computing-software.software-engineering.csharp-dotnet.span-memory-and-allocation-free-code
name: span-memory-and-allocation-free-code
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, span-t, memory-t, stackalloc, arraypool, ref-struct, allocation, gc-pressure, readonlyspan, utf8, allocation-reduction, dotnet-performance]
level: advanced
status: docs-checked
description: "Reduce .NET allocations with Span<T>, ReadOnlySpan<char>, Memory<T>, stackalloc and ArrayPool: parsing without substrings, ref struct rules and async limits."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/memory-and-spans/", "https://learn.microsoft.com/en-us/dotnet/standard/memory-and-spans/memory-t-usage-guidelines", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/stackalloc", "https://learn.microsoft.com/en-us/dotnet/api/system.buffers.arraypool-1"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Span<T>, Memory<T> and allocation-free code

**Goal:** cut GC pressure in hot paths (parsers, serializers, request pipelines) by
slicing existing memory instead of allocating substrings and temporary arrays.

## Span basics
```csharp
ReadOnlySpan<char> line = "2026-10-16,42,ok".AsSpan();
int comma = line.IndexOf(',');
var date = DateOnly.Parse(line[..comma]);            // no substring allocated
int.TryParse(line[(comma + 1)..line.LastIndexOf(',')], out var n);
```
- `Span<T>` is a view over arrays, stack memory or native memory; slicing is free.
- Most BCL parse/format APIs have span overloads (`int.TryParse(ReadOnlySpan<char>)`,
  `TryFormat(Span<char>, out int)`, `Encoding.UTF8.GetBytes(span, span)`).

## stackalloc
```csharp
Span<byte> buf = len <= 256 ? stackalloc byte[256] : new byte[len];
```
Only for small, bounded sizes; never stackalloc an unbounded length from
input (stack overflow kills the process, it can't be caught).

## ArrayPool for larger buffers
```csharp
byte[] rented = ArrayPool<byte>.Shared.Rent(size);   // may be LARGER than size
try { Work(rented.AsSpan(0, size)); }
finally { ArrayPool<byte>.Shared.Return(rented); }
```
Never use the array after returning it; never return twice; slice to the requested size.

## ref struct rules (Span<T> is one)
Cannot be boxed, stored in fields of classes, captured by lambdas or used across `await`.
Use `Memory<T>`/`ReadOnlyMemory<T>` to store or pass across awaits,
and call `.Span` locally.

## Guidelines
- Accept `ReadOnlySpan<T>` parameters for synchronous APIs: callers can pass arrays,
  strings, slices, stack buffers.
- Measure first: BenchmarkDotNet with `[MemoryDiagnoser]` shows Allocated bytes/op.

## Checked
2026-10-28: Confirmed in the Memory<T> and Span<T> usage guidelines, the stackalloc reference and the ArrayPool<T> page: spans over arrays, stack and native memory; Rent/Return; Memory<T> for async use. Removed the stack size figure, the C# 13 relaxation note, string.Create, UTF-8 literals and CollectionsMarshal (not in fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Benchmark shows allocated bytes dropped (ideally to 0 B) and no throughput loss.
- [ ] No stackalloc sized by untrusted input.
