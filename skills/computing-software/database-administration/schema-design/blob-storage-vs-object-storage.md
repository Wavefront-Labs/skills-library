---
id: computing-software.database-administration.schema-design.blob-storage-vs-object-storage
name: blob-storage-vs-object-storage
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, blob-storage, object-storage, binary-data, file-storage, data-types]
level: practitioner
status: draft
description: "Decide whether files and binary data belong in database BLOB columns or object storage with database references, covering size, backups, consistency, streaming and cleanup."
sources:
  - https://www.postgresql.org/docs/current/storage-toast.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/blob/filestream-sql-server
  - https://sqlite.org/intern-v-extern-blob.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Binary data and files: BLOBs vs object storage

## Default for production apps
Store files in object storage (S3, Azure Blob, GCS) and keep metadata plus the object key in the database:
```sql
CREATE TABLE documents (
  id uuid PRIMARY KEY,
  owner_id bigint NOT NULL REFERENCES users,
  storage_key text NOT NULL UNIQUE,     -- e.g. tenants/42/docs/<uuid>
  content_type text NOT NULL,
  size_bytes bigint NOT NULL CHECK (size_bytes >= 0),
  sha256 bytea NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  deleted_at timestamptz);
```

## Why not large BLOBs in the database
- Database storage is the most expensive tier; backups, replicas and restores grow with every file (a 2 TB database of mostly PDFs restores slowly).
- Large values pass through buffer cache and WAL/redo, evicting hot rows and inflating replication traffic.
- Serving files through the app/database is slower than presigned URLs straight from object storage/CDN.

## When BLOBs in the database are fine or better
- Small binaries (thumbnails, signatures, keys < ~100 KB-1 MB) tightly coupled to rows and needing transactional consistency.
- Embedded/local apps: SQLite is faster than the filesystem for many small blobs (the SQLite "35% faster" study for blobs < ~100 KB).
- Strict consistency or compliance requiring one backup unit.

Types: PostgreSQL `bytea` (TOASTed, up to 1 GB) or large objects (`lo_*`, streaming, need explicit cleanup via `lo_unlink`/`vacuumlo`); MySQL `LONGBLOB` (max_allowed_packet limits); SQL Server `varbinary(max)` or FILESTREAM/FileTable (files on NTFS managed by SQL Server); Oracle `BLOB`/SecureFiles.

## Consistency patterns with object storage
- Upload first (to a staging key), then insert the row in a transaction; a periodic sweeper deletes objects without rows after a grace period.
- Delete: mark row `deleted_at`, delete object asynchronously; or use bucket lifecycle rules keyed by prefix/tag.
- Keep a content hash to detect corruption and deduplicate.
- Object versioning/Object Lock for backups and ransomware protection of the files themselves; the database backup does not include them, so back up both and keep their retention aligned.

## Verify
Reconciliation job: every row's `storage_key` exists in the bucket with matching size/hash, and orphaned objects older than the grace period are zero.
