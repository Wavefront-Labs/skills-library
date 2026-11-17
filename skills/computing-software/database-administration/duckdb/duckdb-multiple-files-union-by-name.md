---
id: computing-software.database-administration.duckdb.duckdb-multiple-files-union-by-name
name: duckdb-multiple-files-union-by-name
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, glob, multiple-files, union-by-name, filename, csv, parquet]
level: intro
status: docs-checked
description: "Read many CSV, Parquet or JSON files as one table in DuckDB: glob syntax, file lists, union by position vs name, filename column, glob() function."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/multiple_files/overview.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/multiple_files/combining_schemas.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/parquet/overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: scan a set of files of the same format as a single table, and unify differing schemas safely.

Specify files by glob, by list, or both:

```sql
SELECT * FROM 'dir/*.csv';
SELECT * FROM 'dir/**/*.csv';                      -- any depth
SELECT * FROM '*/*/*.csv';                         -- exactly two levels deep
SELECT * FROM read_parquet(['folder1/*.parquet','folder2/*.parquet']);
SELECT * FROM read_csv(['flights1.csv','flights2.csv']);
```
Glob wildcards: `*` any characters (including none), `**` any number of subdirectories (including none), `?` one character, `[abc]` one of the set, `[a-z]` a range. `?` is not supported for reads over S3 (HTTP encoding issues).

Schema unification:
- Default: the schema of the first file is used and later files are matched by column position (like `UNION ALL`). Files with different column counts then error.
- `union_by_name = true`: columns are matched by name, columns absent from a file become NULL (like `UNION ALL BY NAME`). It uses more memory.

```sql
SELECT * FROM read_csv(['flights3.csv','flights4.csv'], union_by_name = true);
```

Know the source file: the `filename` argument adds a column showing which file each row came from. `filename = 'input_file'` (a string) names the added column, avoiding collisions when the data already has a `filename` column. For Parquet, the `filename` column is a virtual column added automatically since DuckDB 1.3.0 and the option is kept for compatibility.

```sql
SELECT * FROM read_csv(['flights1.csv','flights2.csv'], union_by_name = true, filename = true);
```

List files without reading them: `SELECT * FROM glob('*');` returns one `file` column; it accepts a path with glob patterns.

Gotcha: Parquet multi-file reads only work if the files have the same schema; `read_parquet` also accepts `union_by_name`. The Parquet `schema` option cannot be combined with `union_by_name=true` (see duckdb-parquet-read-write). Hive-style folders: duckdb-hive-partitioning-read.

## Checked

2026-11-07. Read the DuckDB 1.4 docs pages data/multiple_files/overview.md, data/multiple_files/combining_schemas.md and data/parquet/overview.md in full. Confirmed: glob and list examples, wildcard table, `?` unsupported over S3, default positional unification then `union_by_name`, NULL fill, memory cost, `filename` option and string form, `glob()` taking one path parameter and returning a `file` column, Parquet virtual `filename` since 1.3.0, Parquet `schema` vs `union_by_name`. Removed: the claim that `filename = true` is an "older option" for all formats (the page says so only for Parquet), the "list files with one `file` column" wording kept as shown, and the invented Verify step. Added the Parquet overview page to sources.

Method: documentation only; no commands were run.
