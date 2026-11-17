---
id: computing-software.software-engineering.csharp-dotnet.indexers-ranges-and-index-types
name: indexers-ranges-and-index-types
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-collections, indexers, index-from-end, ranges, span, slicing]
level: practitioner
status: docs-checked
description: "Use C# indexers, the ^ index-from-end and .. range operators; which types support them, copy versus no-copy slicing of arrays, strings and spans, and countable types."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/tutorials/ranges-indexes", "https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/indexers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Indexers, Index and Range

## Using ^ and ..
```csharp
int[] a = [10, 20, 30, 40, 50];
a[^1];            // 50: ^n is Length - n
a[1..3];          // [20, 30]: start inclusive, end exclusive; copies for arrays
a[..2]; a[^2..];  // first two, last two
ReadOnlySpan<int> view = a.AsSpan()[1..4];   // no copy
```
- `^0` is the same as `sequence[sequence.Length]`, so `sequence[^0]` throws, but `[0..^0]` (the whole range) is valid because a range end is exclusive.
- The range operator converts its operands to `Index` and builds a `Range`. A negative int converted to `Index` throws `ArgumentOutOfRangeException`.
- Cost depends on the sequence type. For a `string` or an array the result is a copy (O(N) in the range length; for arrays a new array is allocated and changing it does not change the original). For `Span<T>` and `Memory<T>` the result references the same backing store (O(1), no allocation). In performance-sensitive code use `Span<T>` or `Memory<T>`.
- Support: `string`, `Span<T>` and `ReadOnlySpan<T>` support indices and ranges; `List<T>` supports indices but not ranges. Single-dimension and jagged arrays support both; multi-dimensional arrays do not.

## Indexers on your type
```csharp
public class Grid {
    private readonly int[,] _cells = new int[8, 8];
    public int this[int row, int col] {
        get => _cells[row, col];
        set => _cells[row, col] = value;
    }
}
```
- Indexers use the `this` keyword; `value` is the argument of `set`. They can be overloaded and can have one or more parameters.
- A type explicitly supports indices or ranges if it has an indexer taking an `Index` or `Range`; a range indexer may return a different type such as `Span<T>`.
- A type is countable if it has an accessible `int` property named `Length` or `Count`. A countable type without such indexers can get implicit index and range support (the proposal text is the source for the exact rules); with implicit range support the result has the same sequence type as the source.

## Verify
Unit-test slice boundaries (`0..0`, `^0..`, full range) and that an array slice is a copy.

## Checked
2026-11-03. Confirmed against dotnet/docs: "Indices and ranges" tutorial and "Indexers" article. Removed because not found in the pages read: the `Slice(int, int)` signature requirement, `Buffer` sample, `GetRange` and `Take/Skip` advice, `ref`-returning indexers, "indexers cannot be static", the C# 14 span conversion remark, `[MemoryDiagnoser]` check, and the exact exception for `a[1..10]`.
Method: documentation only; no commands were run.
