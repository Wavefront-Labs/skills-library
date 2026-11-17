---
id: computing-software.database-administration.duckdb.duckdb-https-remote-files
name: duckdb-https-remote-files
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, httpfs, https, http-proxy, bearer-token, ca-cert]
level: practitioner
status: docs-checked
description: "Query files over HTTP(S) with DuckDB httpfs: partial Parquet reads, HTTP secrets with bearer tokens or headers, proxy settings, custom CA certificate."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/core_extensions/httpfs/https.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read remote files over HTTP(S) efficiently and through authenticated or proxied networks.

Read-only access to any format DuckDB can read:

```sql
SELECT * FROM 'https://domain.tld/file.extension';
SELECT * FROM read_parquet(['https://domain.tld/file1.parquet','https://domain.tld/file2.parquet']);
```
(Access over HTTP(S) is read-only.)

Partial reading: CSV files are mostly downloaded entirely because the format is row based. Parquet uses metadata plus HTTP Range requests to fetch only needed bytes, so `SELECT column_a FROM 'https://.../file.parquet'` reads only the Parquet metadata and the data for `column_a`, and `SELECT count(*)` can need only metadata.

Authentication with an HTTP secret:

```sql
CREATE SECRET http_auth (TYPE http, BEARER_TOKEN 'token');
CREATE SECRET http_auth (TYPE http,
  EXTRA_HTTP_HEADERS MAP {'Authorization': 'Bearer token'});
```

Proxy, via secret or settings:

```sql
CREATE SECRET http_proxy (TYPE http, HTTP_PROXY 'http_proxy_url',
  HTTP_PROXY_USERNAME 'username', HTTP_PROXY_PASSWORD 'password');
-- or
SET http_proxy = 'http_proxy_url';
SET http_proxy_username = 'username';
SET http_proxy_password = 'password';
```

Custom certificate file: the page says to set these options prior to loading the extension, but its example lists `LOAD httpfs` first:

```sql
LOAD httpfs;
SET ca_cert_file = '/path/to/certificate_file';
SET enable_server_cert_verification = true;
```

Gotcha: CSV files are downloaded entirely in most cases.

## Checked

2026-11-07. Read the HTTP(S) Support page in full and confirmed read-only access, the partial-reading behaviour with HTTP range requests, the metadata-only count(*) case, multi-file scanning, HTTP secrets with BEARER_TOKEN and EXTRA_HTTP_HEADERS, proxy secret and SET options, and the custom certificate options. The page example is sample placeholder URLs, so the fetch tool flagged them as errors. Removed the unsupported write-via-S3 advice, the Parquet footer wording, the Parquet preference advice, the Hive-on-HTTP claim and the Verify step, and stated the page's own order mismatch for the certificate options.

Method: documentation only; no commands were run.
