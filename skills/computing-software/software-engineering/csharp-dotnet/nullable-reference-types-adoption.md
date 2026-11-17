---
id: computing-software.software-engineering.csharp-dotnet.nullable-reference-types-adoption
name: nullable-reference-types-adoption
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, nullable-reference-types, nullable-context, null-forgiving, nullreferenceexception, notnullwhen, required-members, warnaserror]
level: practitioner
status: docs-checked
description: "Turn on C# nullable reference types in an existing codebase incrementally, use the nullable attributes correctly, and avoid null-forgiving (!) abuse."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references", "https://learn.microsoft.com/en-us/dotnet/csharp/nullable-migration-strategies", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/attributes/nullable-analysis"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nullable reference types adoption

**Goal:** make the compiler warn about every possible `NullReferenceException`, and get
an existing project there without a 3,000-warning wall.

## Enable
```xml
<PropertyGroup>
  <Nullable>enable</Nullable>
  <WarningsAsErrors>nullable</WarningsAsErrors>   <!-- once clean -->
</PropertyGroup>
```
New projects: enable from day one. Put it in `Directory.Build.props` for every project.

## Incremental migration
1. Project-level `<Nullable>warnings</Nullable>`: warnings on dereferences, but
   annotations not yet meaningful. Or keep it disabled and opt in per file with
   `#nullable enable` at the top, starting from leaf/utility code.
2. Annotate public APIs first: `string?` where null is valid, `string` where it isn't.
3. Fix warnings by restructuring (guard clauses, early returns), not by `!`.
4. Flip to `enable` project-wide and turn nullable warnings into errors.

## Annotations that teach the compiler
```csharp
public bool TryGet(string key, [NotNullWhen(true)] out User? user)
[return: NotNullIfNotNull(nameof(input))] public static string? Trim(string? input)
public static void ThrowIfNull([NotNull] object? arg)   // after call, arg is not null
[MemberNotNull(nameof(_conn))] private void EnsureOpen() { _conn ??= Open(); }
```
`ArgumentNullException.ThrowIfNull(x)` and `ArgumentException.ThrowIfNullOrEmpty(s)`
are already annotated.

## Constructors and DTOs
- Non-nullable properties not set in the constructor warn (CS8618). Use `required`
  members: `public required string Name { get; init; }` - callers must set them.
- EF Core understands NRT: `string` -> NOT NULL column, `string?` -> NULL. Enabling NRT
  on an existing model can generate migrations that change nullability; review them.

## The null-forgiving operator `!`
`user!.Name` silences the compiler and moves the crash to runtime. Allowed only where
you can prove non-null and the compiler can't (with a comment). `default!` for
properties set by a framework (DI, deserializer) is a common, tolerated idiom.

## Gotchas
- NRT is compile-time only; external callers (reflection, JSON, older assemblies) can
  still pass null. Validate at public boundaries.
- Generics: `T?` on unconstrained T means "default(T)"; use `where T : notnull` or
  `[MaybeNull]` as needed.
- Arrays/collections: `new string[10]` is full of nulls but typed `string[]`.

## Checked
2026-10-28: Confirmed in the nullable references, migration strategies and nullable analysis attributes pages and the ArgumentException.ThrowIfNullOrEmpty API page: enable/warnings contexts, NotNullWhen and related attributes, required members, EF Core nullability mapping. Removed one C# version tag.
Method: documentation only; no commands were run.

## Verify
- [ ] `dotnet build` shows zero CS86xx warnings with nullable warnings as errors.
- [ ] grep for `!.` and `!;` finds only commented, justified uses.
