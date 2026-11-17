---
id: computing-software.software-engineering.csharp-dotnet.custom-attributes-and-reflection-performance
name: custom-attributes-and-reflection-performance
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-reflection, custom-attributes, reflection-performance, compiled-delegates, methodinfo, trimming]
level: advanced
status: docs-checked
description: "Define and read custom C# attributes (AttributeUsage, lazy instances, caching) and annotate reflection for trimming with RequiresUnreferencedCode and DynamicallyAccessedMembers."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/reflection-and-attributes/", "https://learn.microsoft.com/en-us/dotnet/standard/attributes/writing-custom-attributes", "https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/reflection-and-attributes/attribute-tutorial", "https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/prepare-libraries-for-trimming"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom attributes and reflection performance

## Defining an attribute
```csharp
[AttributeUsage(AttributeTargets.Property, AllowMultiple = false, Inherited = true)]
public sealed class ColumnAttribute(string name) : Attribute { public string Name { get; } = name; public bool Required { get; init; } }

public class Person { [Column("full_name", Required = true)] public string Name { get; set; } = ""; }
```
- Attribute classes are public and inherit (directly or indirectly) from `System.Attribute`. By convention the name ends in `Attribute`; at the use site the suffix is optional (`[Column]`).
- `AttributeUsage` has `AttributeTargets`, `Inherited` (default `true`) and `AllowMultiple` (default `false`; applying a single-use attribute twice is a compiler error). With `Inherited = false`, derived classes do not see the attribute on the base.
- Make required values positional constructor parameters and optional values named properties.
- Constructor parameters and public properties are limited to: `bool`, `byte`, `char`, `double`, `float`, `int`, `long`, `short`, `string`, `Type`, enums accessible at the use site, `object` (holding one of the valid types or a one-dimensional array of them) and one-dimensional arrays of these. `sbyte`, `ushort`, `uint`, `ulong`, `decimal`, `nint` and `nuint` are not valid even though they have literals. A constructor with another type compiles but fails when applied.

## Reading attributes
```csharp
var cols = typeof(Person).GetProperties()
    .Select(p => (p, a: p.GetCustomAttribute<ColumnAttribute>()))
    .Where(x => x.a is not null);
```
`GetCustomAttribute` returns null when the attribute is absent. Attribute objects are instantiated lazily, only when you call `GetCustomAttribute(s)`, and a new instance each time (two calls return different instances). So read attributes once per type or member and cache the result rather than in a hot loop.

## Trimming
Reflection over members the trimmer cannot see statically breaks after trimming. Per Microsoft's guidance for trimmable libraries:
- `[RequiresUnreferencedCode]` marks a method that needs dynamic access to code not referenced statically (for example via `System.Reflection`); annotating a caller propagates the warning to its callers.
- `[DynamicallyAccessedMembers]` states which members of a `Type` parameter must be kept (for example public methods); satisfy it by putting the same requirement on your own parameter.

## Verify
Write a small benchmark for the lookup you cache versus the one you repeat, using your own measurements, and run a trimmed publish to see the trim warnings.

## Checked
2026-11-03. Confirmed against dotnet/docs: "Writing custom attributes" (AttributeUsage members, defaults, valid parameter types, naming), the attribute tutorial (lazy, per-call instances, GetCustomAttribute) and "Prepare .NET libraries for trimming" (RequiresUnreferencedCode, DynamicallyAccessedMembers). Removed because not found in the pages read: compiled expression-tree getter code and speed claims, .NET 8 reflection invoke behaviour, `CreateDelegate`, `Activator.CreateInstance<T>`, the JIT/AOT note about `Compile()`, interface-member `Inherited` behaviour, `BindingFlags.NonPublic`, and the benchmark threshold.
Method: documentation only; no commands were run.
