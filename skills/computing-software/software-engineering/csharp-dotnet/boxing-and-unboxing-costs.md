---
id: computing-software.software-engineering.csharp-dotnet.boxing-and-unboxing-costs
name: boxing-and-unboxing-costs
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-type-system, boxing-unboxing, value-types, generics, allocations, struct-interfaces, flags-enums]
level: practitioner
status: docs-checked
description: "Find C# boxing: value types converted to object or an interface, how unboxing fails, how nullable values box, and why it costs an allocation; measure before and after."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/types/boxing-and-unboxing", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/nullable-value-types"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Boxing and unboxing costs

Boxing is the implicit conversion of a value type to `object` or to any interface type it implements. The CLR wraps the value in an object on the managed heap, so each box is an allocation plus a copy. Unboxing is an explicit conversion back; it checks the object is a boxed value of that exact type, then copies the value out.

## Where it hides
```csharp
object o = 42;                         // box
int n = (int)o;                        // unbox
IComparable c = 5;                     // box via an interface the value type implements
```
- The boxed copy and the original are separate memory: changing the original after boxing does not change the box.
- Unboxing `null` throws `NullReferenceException`; unboxing to an incompatible value type throws `InvalidCastException` (a boxed `int` cannot be unboxed with `(short)o`; unbox with `(int)o`).
- A `Nullable<T>` with no value boxes to a null reference; with a value it boxes the underlying `T`, not the `Nullable<T>` instance.

## Remove it
1. Keep values in generic types and methods (`List<int>` rather than a collection of `object`) so the value type is not converted to `object`.
2. Avoid assigning structs to `object` or interface-typed variables and fields in hot paths.

## Verify
Boxing is "computationally expensive" relative to a simple assignment according to Microsoft's guide. Measure with a profiler or allocation benchmark before and after a change, and do not assume a specific saving.

## Checked
2026-11-03. Confirmed against the dotnet/docs page "Boxing and Unboxing (C# Programming Guide)" (definition, heap allocation, separate copies, NullReferenceException, InvalidCastException, performance statement) and the Nullable value types page (boxing of nullable values). Removed because not found in the pages read: claims about enumerators, `Enum.HasFlag` history, `string.Format` and logging overloads, `EqualityComparer<T>.Default` behaviour, enum `ToString` allocation, specific counters and benchmark column names.
Method: documentation only; no commands were run.
