---
id: computing-software.software-engineering.csharp-dotnet.structs-ref-structs-and-ref-parameters
name: structs-ref-structs-and-ref-parameters
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-structs, readonly-struct, record-struct, in-parameters, ref-returns, defensive-copies]
level: advanced
status: docs-checked
description: "Design C# value types: when to use a struct, readonly struct and record struct, defensive copies, in/ref/out parameters and ref returns, and boxing pitfalls."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct", "https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/choosing-between-class-and-struct", "https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/performance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structs, ref structs and ref parameters

**Goal:** value types that save allocations without introducing copy bugs or hidden
boxing.

## When a struct
Framework guidelines: small (under 16 bytes), immutable, logically a single value
(Point, Money, Range), short-lived or embedded in arrays, rarely boxed. Otherwise use a class
(or a record class). Structs are copied on assignment, parameter passing and return.

## readonly struct and record struct
```csharp
public readonly record struct Money(decimal Amount, string Currency)
{
    public Money Add(Money o) => o.Currency == Currency
        ? this with { Amount = Amount + o.Amount }
        : throw new InvalidOperationException("currency mismatch");
}
```
- `readonly struct`: all fields readonly; the compiler can skip defensive copies.
- `record struct`: generated value equality, `ToString`, `with`, deconstruction. Plain structs'
  default `Equals` uses reflection for some layouts - slow; implement `IEquatable<T>` or use record struct.
- `readonly` members on non-readonly structs mark methods that don't mutate.

## Defensive copies
Calling a non-readonly method on a struct accessed through a `readonly` field or an `in`
parameter makes the compiler copy it first (to protect immutability) - silent cost, and
mutations hit the copy:
```csharp
private readonly MutablePoint _p;
_p.Move(1, 1);          // mutates a copy; _p unchanged
```
Make structs `readonly` and the problem disappears.

## Passing by reference
```csharp
static double Length(in Vector3 v) => Math.Sqrt(v.X * v.X + v.Y * v.Y + v.Z * v.Z);   // no copy, read-only
static void Normalize(ref Vector3 v) { ... }                                           // mutate caller's value
static bool TryParse(string s, out Money m) { ... }
ref int slot = ref CollectionsMarshal.AsSpan(list)[i];   // ref local into list storage
slot++;
```
`in` helps only for large readonly structs; for small structs, plain by-value is as fast.
`ref readonly` parameters clarify intent for APIs taking references.

## ref struct
Stack-only types (`Span<T>`, `Utf8JsonReader`): cannot be boxed, stored in fields of classes,
captured by lambdas or used across `await`. Define your own for parsers/buffers wrapping spans.

## Boxing pitfalls
Casting a struct to `object` or an interface allocates a box. Hidden sources: non-generic
collections, `string.Format`/interpolation with older APIs, calling interface methods on a
struct variable typed as the interface. Use generics with
constraints (`where T : IComparable<T>`) to avoid boxing.

## Checked
2026-10-28: Confirmed in the .NET design guidelines (choosing between class and struct: under 16 bytes, immutable, rarely boxed), the struct type reference and the C# performance guidance on in/ref/ref readonly. Removed the C# version tags and the HasFlag boxing claim.
Method: documentation only; no commands were run.

## Verify
- [ ] Custom structs are `readonly` (or justified) and implement `IEquatable<T>`.
- [ ] Allocation profiling shows no unexpected boxing in hot paths.
