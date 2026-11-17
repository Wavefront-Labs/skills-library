---
id: computing-software.software-engineering.csharp-dotnet.generics-constraints-and-variance
name: generics-constraints-and-variance
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-generics, covariance, contravariance, generic-constraints, static-abstract-members, generic-math]
level: practitioner
status: docs-checked
description: "Write C# generics well: constraints (class, struct, notnull, new(), interfaces), in/out variance on interfaces and delegates, static abstract members for generic math."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/generics", "https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/generics/constraints-on-type-parameters", "https://learn.microsoft.com/en-us/dotnet/standard/generics/covariance-and-contravariance", "https://learn.microsoft.com/en-us/dotnet/standard/generics/math"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generics, constraints and variance

**Goal:** reusable, type-safe APIs without boxing, casts or `object`.

## Constraints
```csharp
public sealed class Repository<TEntity, TKey>
    where TEntity : class, IEntity<TKey>      // reference type implementing an interface
    where TKey : notnull, IEquatable<TKey>
{
    public TEntity? Find(TKey id) => ...;
}
T Create<T>() where T : new() => new T();
void Fill<T>(Span<T> s) where T : unmanaged { }   // no references: safe for stackalloc/interop
```
| Constraint | Meaning |
|---|---|
| `class` / `class?` | reference type (non-nullable / nullable) |
| `struct` | non-nullable value type (enables `T?` as `Nullable<T>`) |
| `notnull` | non-nullable reference or value type |
| `unmanaged` | value type with no references |
| `new()` | public parameterless ctor (must be last) |
| `Enum`, `Delegate` | base type constraints |
| `allows ref struct` | (C# 13) T may be a ref struct like `Span<T>` |

Generic value types get specialised code per type (no boxing); reference types share one
implementation.

## Variance (interfaces and delegates only)
```csharp
IEnumerable<string> names = ...;
IEnumerable<object> objs = names;            // covariance: IEnumerable<out T>
Action<object> log = o => Console.WriteLine(o);
Action<string> logString = log;              // contravariance: Action<in T>

public interface IProducer<out T> { T Produce(); }          // T only in output positions
public interface IConsumer<in T> { void Consume(T item); }  // T only in input positions
```
Classes and structs are invariant: `List<string>` is not a `List<object>`. Variance applies only to reference type arguments.

## Static abstract members / generic math (C# 11, .NET 7+)
```csharp
static T Sum<T>(ReadOnlySpan<T> values) where T : INumber<T>
{
    T total = T.Zero;
    foreach (var v in values) total += v;
    return total;
}
Sum<int>([1, 2, 3]); Sum<decimal>([1.5m, 2m]);
```
Define your own: `interface IParsable<TSelf> where TSelf : IParsable<TSelf> { static abstract TSelf Parse(string s); }`.

## Gotchas
- `default(T)` is `null` for references, zero for values; with nullable enabled annotate `T?`
  and understand it means different things for unconstrained T.
- Static fields in a generic type exist once **per closed type** (`Cache<int>` vs `Cache<string>`) -
  handy for per-type caches.
- Prefer generic methods over generic classes when only one method needs the type parameter.

## Checked
2026-10-28: Confirmed in the generics constraints reference (class, struct, notnull, unmanaged, new(), allows ref struct) and the generic math page (INumber<T>, static abstract members). Removed the C# version tag on base-type constraints and the array covariance exception claim.
Method: documentation only; no commands were run.

## Verify
- [ ] No `object` parameters + casts where a constrained generic would do.
- [ ] Custom producer/consumer interfaces declare `out`/`in` where valid.
