---
id: computing-software.data-engineering.polars.io-database-read-write
name: io-database-read-write
category: computing-software
field: data-engineering
product: polars
tags: [polars, io, database, read-database-uri, connectorx, adbc, sqlalchemy, polars-io-database, write-database]
level: practitioner
status: docs-checked
description: "Read from and write to SQL databases in Polars with read_database_uri, read_database and write_database, choosing ConnectorX, ADBC or SQLAlchemy engines."
sources:
  - https://docs.pola.rs/user-guide/io/database/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move data between Polars and a database. Polars does not manage connections itself; external libraries (engines) do.

Read
- `pl.read_database_uri(query=..., uri=...)`: connection string. Default engine ConnectorX; pass `engine="adbc"` for ADBC.
- `pl.read_database(query=..., connection=...)`: use when you already have an engine/connection, e.g. SQLAlchemy.

```python
uri = "postgresql://username:password@server:port/database"
pl.read_database_uri(query="SELECT * FROM foo", uri=uri)
pl.read_database_uri(query="SELECT * FROM foo", uri=uri, engine="adbc")

from sqlalchemy import create_engine
conn = create_engine("sqlite:///test.db")
pl.read_database(query="SELECT * FROM foo", connection=conn.connect())
```
`read_database_uri` is likely faster than `read_database` with SQLAlchemy/DBAPI2 connections, which may load rows into Python row-wise before copying into column-wise Arrow.

Engines for reading via URI
- ConnectorX (default): Rust, Arrow-native, zero-copy to Polars; supports Postgres, Mysql, SQL Server, Redshift and more. Install the extra dependency or `pip install connectorx`.
- ADBC (Arrow Database Connectivity): early days, limited support; drivers only for Postgres, SQLite and Snowflake. Install the driver, e.g. `pip install adbc-driver-sqlite`.

Write
`DataFrame.write_database(table_name=..., connection=uri, engine=...)`.
```python
df = pl.DataFrame({"foo": [1, 2, 3]})
df.write_database(table_name="records", connection=uri)                 # SQLAlchemy (default)
df.write_database(table_name="records", connection=uri, engine="adbc")  # ADBC
```
- SQLAlchemy engine (default): any SQLAlchemy-supported database; needs `pip install SQLAlchemy pandas`. Polars converts to a PyArrow-backed Pandas DataFrame and writes with SQLAlchemy methods.
- ADBC: same databases as ADBC reading; install the matching driver.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
