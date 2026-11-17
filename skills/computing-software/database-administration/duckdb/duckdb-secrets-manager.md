---
id: computing-software.database-administration.duckdb.duckdb-secrets-manager
name: duckdb-secrets-manager
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, secrets, create-secret, persistent-secret, scope, credentials]
level: practitioner
status: docs-checked
description: "Manage DuckDB secrets: types, temporary vs persistent, scopes with longest-prefix matching, which_secret, duckdb_secrets, and secret_directory."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/configuration/secrets_manager.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: store credentials once, scope them per bucket or host, and see which one a path will use.

Secret types and their providers (extension): `s3`, `r2`, `gcs`, `http`, `huggingface`, `iceberg` (httpfs / iceberg), `azure` (azure), `mysql`, `postgres`, `ducklake`. Each type has one or more providers; for S3, GCS, R2 and Azure these are `CONFIG` (you pass everything; the default when no provider is named) and `credential_chain` (auto-fetch).

Create:

```sql
CREATE SECRET my_secret (TYPE s3, KEY_ID 'my_secret_key', SECRET 'my_secret_value', REGION 'my_region');
CREATE PERSISTENT SECRET my_persistent_secret (TYPE s3, KEY_ID 'k', SECRET 'v');
```
Temporary secrets (default) live in memory for the DuckDB instance. Persistent secrets are written unencrypted in binary format to a secrets directory and are auto-loaded on startup, so treat that directory as sensitive. Change it with `SET secret_directory = 'path/to/my_secrets_dir';` (default `~/.duckdb/stored_secrets`; setting `home_directory` does not move it).

Scopes: a `SCOPE` is a path prefix. For a path, the secret whose scope is the longest matching prefix wins:

```sql
CREATE SECRET secret1 (TYPE s3, KEY_ID 'k1', SECRET 's1', SCOPE 's3://my-bucket');
CREATE SECRET secret2 (TYPE s3, KEY_ID 'k2', SECRET 's2', SCOPE 's3://my-other-bucket');
FROM which_secret('s3://my-other-bucket/file.parquet', 's3');   -- shows secret2 is chosen
```
This allows joining data across organizations in one query.

List and remove:

```sql
FROM duckdb_secrets();                      -- sensitive fields redacted
DROP PERSISTENT SECRET my_persistent_secret;
```

Use with: duckdb-s3-secrets-httpfs, duckdb-https-remote-files, duckdb-hugging-face-hf-protocol, duckdb-iceberg-rest-catalogs.

## Checked

2026-11-07. Read the DuckDB 1.4 docs page configuration/secrets_manager.md in full. Confirmed: secret type table with extensions, providers (CONFIG default, credential_chain) for S3, GCS, R2 and Azure, temporary versus persistent secrets, unencrypted binary storage, the `~/.duckdb/stored_secrets` directory and auto-load on startup, `secret_directory`, `home_directory` has no effect, scope longest-prefix matching, `which_secret(path, type)`, `duckdb_secrets()` redaction, DROP PERSISTENT SECRET, cross-organization joins. Removed: `allow_persistent_secrets`, `default_secret_storage` and `allow_unredacted_secrets` settings with defaults (not on this page), the invented Verify step; stated the default directory as the page does.

Method: documentation only; no commands were run.
