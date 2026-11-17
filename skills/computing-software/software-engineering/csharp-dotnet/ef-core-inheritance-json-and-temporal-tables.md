---
id: computing-software.software-engineering.csharp-dotnet.ef-core-inheritance-json-and-temporal-tables
name: ef-core-inheritance-json-and-temporal-tables
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, ef-core-modeling, ef-inheritance-mapping, ef-json-columns, ef-temporal-tables, tph, tpt, complex-types]
level: advanced
status: draft
description: "EF Core mapping for inheritance (TPH, TPT, TPC), JSON columns and complex types, and SQL Server temporal tables, with query behaviour and migration caveats by EF version."
sources: ["https://learn.microsoft.com/en-us/ef/core/modeling/inheritance", "https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-8.0/whatsnew#json-columns", "https://learn.microsoft.com/en-us/ef/core/providers/sql-server/temporal-tables"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inheritance, JSON columns, temporal tables

## Inheritance
```csharp
modelBuilder.Entity<Payment>().UseTphMappingStrategy()                      // default: one table + Discriminator column
    .HasDiscriminator<string>("Kind").HasValue<Card>("card").HasValue<Bank>("bank");
// modelBuilder.Entity<Payment>().UseTptMappingStrategy();  // table per type: joins, normalised, slower
// modelBuilder.Entity<Payment>().UseTpcMappingStrategy();  // table per concrete type (EF 7+): no joins for leaf queries, needs non-identity keys (Guid/sequence)
var cards = await db.Payments.OfType<Card>().ToListAsync();
```
TPH is fastest and the default; columns for subtype properties are nullable. TPT adds joins on every query; TPC avoids joins but unions for base-type queries.

## JSON columns (EF 7+ SQL Server/Postgres/SQLite; EF 8 broadened)
```csharp
modelBuilder.Entity<Order>().OwnsOne(o => o.Shipping, b => b.ToJson());           // owned type in one JSON column
modelBuilder.Entity<Order>().OwnsMany(o => o.Lines, b => b.ToJson());
modelBuilder.Entity<Customer>().ComplexProperty(c => c.Address);                  // EF 8 complex types (value semantics, table splitting)
var big = await db.Orders.Where(o => o.Shipping.City == "Oslo").ToListAsync();    // translated to JSON_VALUE
```
Good for rarely-joined, document-shaped data. Queries inside JSON are translated but can't use ordinary indexes (add computed-column indexes). EF 10 adds complex types in JSON. Partial updates: EF 8 uses `JSON_MODIFY` for scalar changes.

## Temporal tables (SQL Server)
```csharp
modelBuilder.Entity<Product>().ToTable("Products", t => t.IsTemporal());
var past  = db.Products.TemporalAsOf(DateTime.UtcNow.AddDays(-7));
var hist  = db.Products.TemporalAll().Where(p => p.Id == 1).OrderBy(p => EF.Property<DateTime>(p, "PeriodStart"));
```
The history table is maintained by SQL Server; period columns are shadow properties in UTC. Time-travel queries are read-only (no tracking updates to history). Migrations that alter the table require turning versioning off/on, which EF scripts for you; review them.

## Gotchas
- Changing mapping strategy rewrites tables: it is a data migration.
- Discriminators must be indexed for large TPH tables.
- JSON columns need compatibility level 160+ (SQL Server 2022/Azure SQL).
- Owned collections in JSON cannot be queried with joins to other entities easily.

## Verify
Inspect generated SQL (`ToQueryString()`, logging) and the migration script; round-trip an entity of each subtype and a JSON edit in an integration test against the real provider.
