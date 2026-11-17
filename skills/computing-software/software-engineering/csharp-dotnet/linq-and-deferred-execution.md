---
id: computing-software.software-engineering.csharp-dotnet.linq-and-deferred-execution
name: linq-and-deferred-execution
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, linq, deferred-execution, ienumerable, iqueryable, multiple-enumeration, client-evaluation, tolist, csharp-linq]
level: practitioner
status: docs-checked
description: "Use LINQ without surprises: deferred vs immediate execution, multiple enumeration, IEnumerable vs IQueryable in EF Core, and LINQ performance in hot paths."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/linq/get-started/introduction-to-linq-queries", "https://learn.microsoft.com/en-us/dotnet/standard/linq/deferred-execution-lazy-evaluation", "https://learn.microsoft.com/en-us/ef/core/querying/client-eval"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# LINQ and deferred execution

**Goal:** readable queries over collections and databases that run once, where you
expect, and without pulling a whole table into memory.

## Deferred vs immediate
- Deferred (build a query, run on enumeration): `Where`, `Select`, `OrderBy`, `Skip`,
  `Take`, `GroupBy`, `Join`.
- Immediate (run now): `ToList`, `ToArray`, `ToDictionary`, `Count`, `Sum`, `First`,
  `Any`, `Max`, `foreach`.
```csharp
var active = users.Where(u => u.IsActive);   // nothing ran yet
users.Add(newUser);
active.Count();                               // includes newUser: query runs now
```

## Multiple enumeration
```csharp
IEnumerable<Order> orders = LoadOrders();      // maybe a DB query or yield method
if (orders.Any()) Process(orders.First(), orders.Count());   // runs the source 3 times
```
Materialise once (`var list = orders.ToList();`) when you will enumerate more than once
or when the source is expensive/non-repeatable. Analyzers (CA1851, ReSharper) flag it.

## IQueryable vs IEnumerable (EF Core)
```csharp
IQueryable<User> q = db.Users.Where(u => u.Age > 30);   // translated to SQL
IEnumerable<User> e = db.Users.AsEnumerable().Where(u => u.Age > 30);  // loads ALL users, filters in memory
```
- Keep composing on `IQueryable` until the final `ToListAsync()`.
- A method taking `IEnumerable<T>` and calling `.Where` on a DbSet silently switches to
  in-memory filtering.
- EF Core throws if a non-translatable expression appears anywhere but the final
  Select; fix by rewriting, not by inserting `AsEnumerable()` early.
- Project with `Select(u => new UserDto(u.Id, u.Name))` to fetch only needed columns.

## Common mistakes
- `First()` throws on empty; `FirstOrDefault()` returns null/default. `Single()` also
  throws on duplicates - use it to assert uniqueness.
- `Count() > 0` vs `Any()`: `Any` short-circuits on enumerables.
- Side effects inside `Select` run per enumeration (and not at all if never enumerated).
- Closures capture variables: modifying a captured variable before enumeration changes
  the query.

## Performance
LINQ allocates enumerators and delegates; in hot loops, plain `for`/`foreach` over
arrays or `Span<T>` wins. Measure with a benchmark.

## Verify
- [ ] EF Core logging (`LogTo(Console.WriteLine)`) shows filters in the generated SQL WHERE, not in memory.
- [ ] CA1851 (possible multiple enumeration) enabled.

## Checked

- Date: 2026-10-28
- Confirmed on Microsoft Learn (LINQ introduction, deferred execution, EF Core client evaluation, CA1851 pages): deferred vs immediate operators, multiple enumeration, client evaluation only in the final Select.
- Removed: EF Core 3 version tag, .NET 9 performance remark.
Method: documentation only; no commands were run.
