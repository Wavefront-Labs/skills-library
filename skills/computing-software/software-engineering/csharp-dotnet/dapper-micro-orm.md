---
id: computing-software.software-engineering.csharp-dotnet.dapper-micro-orm
name: dapper-micro-orm
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-ado-net, dapper, micro-orm, multi-mapping, querymultiple, sql-parameters]
level: practitioner
status: draft
description: "Use Dapper for fast SQL access in .NET: parameterised queries, multi-mapping, QueryMultiple, transactions, bulk and IN lists, type handlers, and when EF Core is the better tool."
sources: ["https://github.com/DapperLib/Dapper", "https://www.learndapper.com/", "https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/ado-net-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dapper

Dapper extends `IDbConnection` with `Query`, `QueryFirstOrDefault`, `Execute`, `QueryMultiple` and maps columns to objects by name with cached IL emit. Minimal overhead over raw ADO.NET.

```csharp
using var conn = new SqlConnection(cs);
var users = await conn.QueryAsync<User>("SELECT Id, Name FROM Users WHERE Age > @Age", new { Age = 30 });   // parameters from anonymous object
var one   = await conn.QuerySingleOrDefaultAsync<User>("SELECT * FROM Users WHERE Id = @id", new { id });
var ids   = await conn.QueryAsync<User>("SELECT * FROM Users WHERE Id IN @ids", new { ids = new[] { 1, 2, 3 } });   // list expansion
var n     = await conn.ExecuteAsync("UPDATE Users SET Name = @Name WHERE Id = @Id", users);                       // runs once per element

// multi-mapping: join into object graph
var orders = await conn.QueryAsync<Order, Customer, Order>(
    "SELECT o.*, c.* FROM Orders o JOIN Customers c ON c.Id = o.CustomerId",
    (o, c) => { o.Customer = c; return o; }, splitOn: "Id");               // splitOn = first column of the next object

// several result sets
using var grid = await conn.QueryMultipleAsync("SELECT * FROM A; SELECT * FROM B WHERE X=@x", new { x = 1 });
var a = await grid.ReadAsync<A>(); var b = await grid.ReadAsync<B>();

// transaction, stored procedure, output
using var tx = conn.BeginTransaction();
await conn.ExecuteAsync("usp_Do", new { P = 1 }, tx, commandType: CommandType.StoredProcedure);
tx.Commit();
```
## Rules
- Always parameters; never string-interpolate user input. Identifiers cannot be parameters.
- Dapper does not open the connection if you don't (it opens/closes if closed); with transactions open it yourself.
- Property/column name mismatch: alias in SQL, or `DefaultTypeMap.MatchNamesWithUnderscores = true`.
- `DateOnly`/`TimeOnly`/enums: add `SqlMapper.AddTypeHandler`.
- Use `DynamicParameters` for output params and `commandTimeout`. Buffered by default; `buffered: false` streams large sets.
- Dapper.AOT is an optional source-generator variant for AOT.

## When EF Core instead
Change tracking, migrations, LINQ composition, aggregates; use Dapper for reporting queries, hot paths and bulk reads (they combine well: share the connection via `db.Database.GetDbConnection()`).

## Gotchas
- `Query` returns default (zeroed) for NULL into non-nullable value types: throws or defaults; type as nullable.
- `splitOn` wrong -> null objects.
- Large `IN` lists hit the 2100 parameter limit (SQL Server); use TVP or temp tables.

## Verify
Unit-test mapping with a SQLite in-memory DB; confirm the SQL profile shows parameterised statements.
