---
id: computing-software.software-engineering.csharp-dotnet.linq-grouping-joins-and-new-operators
name: linq-grouping-joins-and-new-operators
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-linq, linq-groupby-join, linq-countby-aggregateby, tolookup, lookup, set-operations]
level: practitioner
status: docs-checked
description: "Use LINQ GroupBy, ToLookup, Join, GroupJoin and set operators, and know the newer ones: .NET 6 By variants and Chunk, .NET 9 CountBy/AggregateBy/Index, .NET 10 LeftJoin."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/grouping-data", "https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/join-operations", "https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/set-operations", "https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/converting-data-types", "https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-9/libraries", "https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-6"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LINQ grouping, joins and newer operators

```csharp
var byCity = people.GroupBy(p => p.City);                       // one IGrouping per key; group.Key is the city
foreach (var g in byCity) foreach (var p in g) { /* nested foreach reaches group items */ }

var rows = orders.Join(customers, o => o.CustomerId, c => c.Id, (o, c) => new { c.Name, o.Total });   // inner join
var withAll = customers.GroupJoin(orders, c => c.Id, o => o.CustomerId,
                (c, os) => new { c.Name, Orders = os });       // every customer appears, os may be empty
var lookup = orders.ToLookup(o => o.CustomerId);                // one-to-many dictionary, built immediately
```

## Grouping
- `GroupBy` (query syntax `group ... by ...`) puts elements that share a key into groups; each group is an `IGrouping<TKey, TElement>`. The default equality comparer for the key type is used unless you supply one.
- Keys may be a property, a computed value, a Boolean expression or an anonymous type (a compound key). Nested groups need nested `foreach` loops to reach the items.
- `ToLookup` stores elements in a `Lookup<TKey, TElement>`, a one-to-many dictionary, and forces query execution (like `ToArray`, `ToList`, `ToDictionary`), so it fits "build once, query many".

## Joins
- `Join` and `GroupJoin` perform equijoins: keys are matched by equality only (T-SQL supports other operators, LINQ's join does not).
- `Join` is an inner join: an element with no match in the other sequence does not appear.
- `GroupJoin` returns one result per element of the first sequence, with the matching elements of the second grouped (empty if none). It has no direct relational equivalent; it is a superset of inner and left outer joins.
- Left outer join: before .NET 10, call `DefaultIfEmpty` on the group join's result. .NET 10 adds `LeftJoin` and `RightJoin` to `Enumerable` and `Queryable`.

## Set operators
- `Distinct`, `Except`, `Intersect`, `Union`. Each has a `...By` variant taking a key selector (`DistinctBy`, `ExceptBy`, `IntersectBy`, `UnionBy`), added in .NET 6. `ExceptBy` and `IntersectBy` take two sequences of possibly different types; `DistinctBy` returns the first element for each key.

## Newer operators
- .NET 6: `Chunk` (split into chunks of a maximum size), `MinBy` and `MaxBy`, `TryGetNonEnumeratedCount` (count without forcing enumeration), `ElementAt` with `Index` (e.g. `ElementAt(^2)`), and `FirstOrDefault`/`LastOrDefault`/`SingleOrDefault` overloads that take a default value.
- .NET 9: `CountBy` (frequency of each key) and `AggregateBy` (aggregate state by key) do this without allocating intermediate groupings via `GroupBy`; `Index` extracts the implicit index of each item.

## Verify
Unit-test group counts against a hand-computed table, and test that a customer with no orders appears in the `GroupJoin` result but not in the `Join` result.

## Checked
2026-11-03. Confirmed against dotnet/docs: Grouping data, Join operations, Set operations, Converting data types, What's new in .NET 6 and .NET 9 libraries. Removed because not found there (API reference pages are not in dotnet/docs): hash complexity of `Join`, nested-loop cost, multiple-enumeration advice, `Count() > 0` versus `Any()`, `OrderBy().First()` versus `MinBy`, allocation and `static` lambda remarks, EF Core translation remarks, `GroupBy` buffering and ordering behaviour, `Distinct` order, `CountBy` return type, `AggregateBy` and `Index` call forms, and the BenchmarkDotNet suggestion.
Method: documentation only; no commands were run.
