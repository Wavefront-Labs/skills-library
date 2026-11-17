---
id: computing-software.software-engineering.fsharp.sql-data-access
name: sql-data-access
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, sql-data-access, fsharp-data, dapper, parameterised-queries]
level: practitioner
status: draft
description: "Query SQL databases from F# using parameterised ADO.NET or Dapper, with records and CLIMutable, and notes on EF Core."
sources:
  - https://learn.microsoft.com/en-us/dotnet/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SQL data access
**Goal:** safe database access.

```fsharp
open System.Data
open Microsoft.Data.SqlClient
open Dapper

[<CLIMutable>]
type User = { Id: int; Name: string }

let getUser (conn: IDbConnection) id =
    conn.QuerySingleOrDefault<User>("SELECT Id, Name FROM Users WHERE Id = @id", {| id = id |})

let insert (conn: IDbConnection) (name: string) =
    conn.Execute("INSERT INTO Users(Name) VALUES (@name)", {| name = name |})

let rows (connStr: string) =
    use conn = new SqlConnection(connStr)
    conn.Open()
    use cmd = new SqlCommand("SELECT Name FROM Users WHERE Id = @id", conn)
    cmd.Parameters.AddWithValue("@id", 1) |> ignore
    use r = cmd.ExecuteReader()
    [ while r.Read() -> r.GetString 0 ]
```
- Always use parameters, never string concatenation or interpolation.
- Dapper maps columns to `[<CLIMutable>]` records or classes; `QuerySingleOrDefault` returns null for missing, so wrap with `Option.ofObj` (or `box` check for records).
- EF Core works with F# but needs `[<CLIMutable>]` entities and care with F# options/unions (value converters); many teams prefer Dapper or Npgsql.FSharp (third party).
- Dispose connections with `use`.

## Gotchas
- F# options are not mapped by Dapper; map them manually.
- `QuerySingleOrDefault` of a record type returns null (a non-F# null) for no rows; check `isNull (box x)`.

## Self-check
Run an `Id` query against SQLite in-memory and confirm both found and missing cases.
