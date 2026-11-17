---
id: computing-software.software-engineering.ocaml.databases-with-caqti
name: databases-with-caqti
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, caqti-database, caqti, postgresql, sqlite, sql-queries]
level: advanced
status: docs-checked
description: "Use Caqti for typed SQL queries over PostgreSQL, SQLite3 or MariaDB: URI-selected drivers, typed requests, Lwt connectors."
sources: ["https://github.com/paurkedal/ocaml-caqti"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Caqti

```ocaml
(* libraries: caqti caqti-lwt caqti-driver-postgresql (or caqti-driver-sqlite3) *)
open Lwt.Infix
open Caqti_request.Infix

let plus = Caqti_request.(Caqti_type.(t2 int int) ->! Caqti_type.int) "SELECT ? + ?"

module Db =
  (val Caqti_lwt_unix.connect (Uri.of_string "postgresql://")
       >>= Caqti_lwt.or_fail |> Lwt_main.run)

let () = ignore (Db.find plus (7, 13))   (* Ok 20 in the README example *)
```

## Notes
- Caqti is a monadic cooperative-threaded connector API for relational databases. The connection URI picks the driver and is typically provided at run time; `connect` returns a first-class module implementing the connection API.
- Caqti does not generate or analyse SQL. It provides templating and uniform parameter handling, encoding and decoding values according to declared types.
- Drivers and URI schemes: MariaDB `mariadb://` (`caqti-driver-mariadb`, also MySQL), PostgreSQL `postgresql://` (`caqti-driver-postgresql`, C bindings), PostgreSQL `pgx://` (`caqti-driver-pgx`, experimental, recommended only for MirageOS), SQLite3 `sqlite3://` (`caqti-driver-sqlite3`).
- Connectors: `caqti` (blocking unix), `caqti-lwt`, `caqti-async`, and experimental `caqti-eio`, `caqti-miou`, `caqti-mirage`.
- Link against the driver you need or against `caqti.plugin` to load drivers at run time. Under utop dynamic linking does not work: `#require` the driver explicitly.
- `ppx_rapper` is a syntax extension that simplifies Caqti query type specifications.
- The API has changed between releases (the README notes older tutorials are out of date); check the API docs of your installed version.

## Self-check
- [ ] A parameterised query returns the expected row from a test database.

## Checked

2026-11-08. Read in full: the ocaml-caqti README (synopsis, driver table, package list, utop example).
Removed: connect_pool, transaction call names, placeholder-safety advice, other-driver and migration-tool recommendations (not in the cited page).
Method: documentation only; no commands were run.
