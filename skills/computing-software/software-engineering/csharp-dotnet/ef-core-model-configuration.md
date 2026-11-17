---
id: computing-software.software-engineering.csharp-dotnet.ef-core-model-configuration
name: ef-core-model-configuration
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, ef-fluent-api, owned-types, value-conversions, ientitytypeconfiguration, ef-core, complex-types, ef-core-modeling]
level: practitioner
status: docs-checked
description: "Configure EF Core models precisely: fluent API in IEntityTypeConfiguration classes, keys, indexes and lengths, owned and complex types, converters and query filters."
sources: ["https://learn.microsoft.com/en-us/ef/core/modeling/", "https://learn.microsoft.com/en-us/ef/core/modeling/owned-entities", "https://learn.microsoft.com/en-us/ef/core/modeling/value-conversions", "https://learn.microsoft.com/en-us/ef/core/querying/filters"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# EF Core model configuration

**Goal:** a schema you'd design by hand - right types, lengths, indexes - produced from
a domain model that stays clean.

## Where configuration lives
```csharp
protected override void OnModelCreating(ModelBuilder b) =>
    b.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);

internal sealed class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> e)
    {
        e.ToTable("orders");
        e.HasKey(o => o.Id);
        e.Property(o => o.Number).HasMaxLength(20).IsRequired();
        e.HasIndex(o => o.Number).IsUnique();
        e.Property(o => o.Total).HasPrecision(18, 2);
        e.Property(o => o.Status).HasConversion<string>().HasMaxLength(20);   // enum as text
        e.HasQueryFilter(o => !o.IsDeleted);                                    // soft delete
    }
}
```
Fluent API beats attributes for anything beyond trivial: keeps persistence concerns out of
domain classes and supports everything. Conventions: `Id`/`<Type>Id` keys, `string` ->
`nvarchar(max)` on SQL Server (set lengths!), nullability from NRT.

## Owned types and complex types
```csharp
e.OwnsOne(o => o.ShippingAddress, a =>
{
    a.Property(x => x.Street).HasMaxLength(200);
    a.Property(x => x.PostCode).HasMaxLength(10);
});                                                   // stored in the orders table by default
e.OwnsMany(o => o.Lines, l => l.ToTable("order_lines"));
e.ComplexProperty(o => o.Price);                      // EF 8+ complex type: value object, no identity
```
Owned/complex types model DDD value objects without separate identity.

## Value converters
```csharp
e.Property(o => o.CustomerId).HasConversion(id => id.Value, v => new CustomerId(v));   // strongly typed IDs
configurationBuilder.Properties<DateTime>().HaveConversion<UtcDateTimeConverter>();   // ConfigureConventions: global
```
Converted properties can't always be translated in queries (e.g. calling methods on them).

## Global query filters
Multi-tenancy and soft delete: `HasQueryFilter(o => o.TenantId == _tenantId)` (field on the
context). Bypass with `.IgnoreQueryFilters()`. Filters on required navigations can make
related rows silently disappear from `Include`.

## Shadow and concurrency properties
`e.Property<DateTime>("UpdatedAt")` (shadow), set in `SaveChanges` interceptors;
`e.Property(o => o.Version).IsRowVersion()` for optimistic concurrency.

## Verify
- [ ] Generated migration SQL reviewed: no `nvarchar(max)`/`text` where a length belongs, indexes present.
- [ ] Model snapshot diff in PRs shows only intended changes.

## Checked
2026-10-28 Confirmed on the EF Core modeling, entity properties, keys, indexes, owned entities, value conversions, bulk configuration, shadow properties, concurrency, query filters and EF Core 8 what's-new pages: `ApplyConfigurationsFromAssembly`, `IEntityTypeConfiguration<T>`, `HasMaxLength`, `HasPrecision`, `HasConversion<string>`, `OwnsOne`/`OwnsMany`, `ComplexProperty` (EF 8), `HaveConversion` in `ConfigureConventions`, `HasQueryFilter`/`IgnoreQueryFilters`, query filters and required navigations, `IsRowVersion`, SaveChanges interceptor for shadow properties, `nvarchar(max)` default for strings. Removed: the `OwnsOne(...ToJson())` line and the owned-column naming comment (not on the fetched pages).
Method: documentation only; no commands were run.
