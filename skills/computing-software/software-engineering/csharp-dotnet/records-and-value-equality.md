---
id: computing-software.software-engineering.csharp-dotnet.records-and-value-equality
name: records-and-value-equality
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, csharp-records, record-struct, value-equality, with-expression, init-only, immutability, value-objects]
level: practitioner
status: docs-checked
description: "Use C# records and record structs for immutable data: positional syntax, with-expressions, value equality pitfalls with collections, and when a class is better."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record", "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/records"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Records and value equality

**Goal:** DTOs, messages and value objects with correct equality and non-destructive
updates, without hand-written Equals/GetHashCode.

## Syntax
```csharp
public record Money(decimal Amount, string Currency);           // reference type, positional
public readonly record struct Point(double X, double Y);        // value type, immutable
public record Customer
{
    public required string Id { get; init; }
    public string? Email { get; init; }
}
var m2 = m1 with { Amount = 20m };                              // copy with change
var (amount, ccy) = m1;                                         // deconstruct
```
Positional `record` properties are `init`-only; positional `record struct` (without
`readonly`) properties are mutable.

## Validation
`with` expressions do NOT call your constructor: they clone via the generated copy
constructor and then run the `init` accessors of the properties you set. So validation
that lives only in a constructor can be bypassed by `with`. Put it in the init accessor:
```csharp
public record Email
{
    private readonly string _value = "";
    public required string Value
    {
        get => _value;
        init => _value = IsValid(value) ? value : throw new ArgumentException("bad email", nameof(Value));
    }
}
```

## Equality pitfalls
- Two records are equal if they have the same type and store the same values. A
  reference-type property such as an array compares by reference, so two records holding
  different arrays with equal contents are unequal. Override equality or share one instance.
- Inheritance: equality depends on the runtime type, so an `A` and a derived `B` with the
  same A-properties are not equal (the compiler-synthesized `EqualityContract`).
- `with` is a SHALLOW copy: the new record shares mutable reference properties.

## When to use what
| Use | Type |
|---|---|
| DTOs, messages, events, value objects | `record` / `record struct` |
| Small value-type data with immutable properties | `readonly record struct` |
| Entities with identity and lifecycle (EF Core entities) | `class` (EF Core depends on reference equality, so records are not appropriate entity types) |

## ToString and logging
The synthesized `ToString` prints the type name and its public properties and fields
(through `PrintMembers`). That includes secrets; provide your own `PrintMembers` or avoid
logging records that hold sensitive data.

## Verify
- [ ] Unit test: two instances with the same data are `==` and have equal hash codes.
- [ ] No record used as a dictionary key has a collection-typed property.

## Checked
2026-11-01. Confirmed against the C# record language-reference page: positional property mutability (init-only for record class and readonly record struct, read-write for record struct), `with` via clone and copy constructor then setting properties, shallow copy, same-type-and-values equality, runtime-type equality with `EqualityContract`, `PrintMembers`/`ToString`, and EF Core needing reference equality. Removed: the `EqualityComparer<T>.Default` and `ImmutableArray<T>` advice and the no-heap-allocation claim.
Method: documentation only; no commands were run.
