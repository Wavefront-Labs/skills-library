---
id: computing-software.software-engineering.csharp-dotnet.equality-comparers-and-dictionary-keys
name: equality-comparers-and-dictionary-keys
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-collections, iequatable, iequalitycomparer, gethashcode, dictionary-keys, record-struct]
level: practitioner
status: docs-checked
description: "Design C# dictionary and set keys: record structs for value equality, IEquatable with Equals/GetHashCode overrides, IEqualityComparer for types you do not own."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/records", "https://learn.microsoft.com/en-us/dotnet/standard/collections/comparisons-and-sorts-within-collections", "https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2218", "https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1066"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Equality comparers and dictionary keys

## Value keys
```csharp
public readonly record struct CustomerKey(string Tenant, int Id);
```
- A plain class uses reference equality by default (`==` checks whether two variables point to the same object).
- A `record struct` gets compiler-generated value equality without using reflection, which Microsoft notes is faster than plain struct equality. `readonly record struct` makes the positional properties `init`-only. Use `record struct` for small self-contained values.
- Avoid records as entity types in Entity Framework Core, which depends on reference equality to track entities.

## Custom equality on a class
Implement `IEquatable<T>`, and when you override `Equals` also override `GetHashCode`. The analyzers back this up: CA1066 (implement `IEquatable` when overriding `Equals`), CA1067 (override `Equals` when implementing `IEquatable`) and CA2218 (override `GetHashCode` on overriding `Equals`); CA1815 covers `Equals` and `==` on value types.
```csharp
public sealed class Sku : IEquatable<Sku> {
    public string Code { get; }
    public Sku(string code) => Code = code.ToUpperInvariant();
    public bool Equals(Sku? o) => o is not null && Code == o.Code;
    public override bool Equals(object? o) => Equals(o as Sku);
    public override int GetHashCode() => Code.GetHashCode();
}
```
Keep key fields immutable: equal objects must produce equal hash codes, so a key that changes after insertion cannot be found again.

## Comparers for types you do not own
Dictionary-style collections have constructor overloads that take an `IEqualityComparer<T>` used to compare keys.
```csharp
var ci = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
var map = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);
```
For string keys choose a comparer deliberately: `Ordinal` or `OrdinalIgnoreCase` for identifiers (Microsoft's string guidance recommends them as the safe culture-agnostic default).

## Verify
Test that `Equals` true implies equal hash codes for sample pairs, and that lookups with different casing work when the comparer says they should.

## Checked
2026-11-03. Confirmed against dotnet/docs: "Records" (record struct equality, reference equality for plain classes, EF Core note), "Comparisons and sorts within collections" (IEqualityComparer in dictionary constructors), string best-practice page (Ordinal defaults) and the rule pages CA1066, CA1067, CA2218, CA1815. Removed because the pages read (the dotnet/docs repo has no API reference) do not state them: `HashCode.Combine` randomisation, hash-flooding resistance of the default string comparer, NaN and -0.0 key pitfalls, boxing and reflection cost of struct default equality, collections-as-keys and iteration-order remarks.
Method: documentation only; no commands were run.
