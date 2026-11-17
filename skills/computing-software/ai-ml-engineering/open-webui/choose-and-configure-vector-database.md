---
id: computing-software.ai-ml-engineering.open-webui.choose-and-configure-vector-database
name: choose-and-configure-vector-database
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [env-configuration, vector-db, pgvector, chromadb, qdrant, rag]
level: advanced
status: docs-checked
description: "Pick the Open WebUI VECTOR_DB backend and set the ChromaDB HTTP, PGVector index and Qdrant multitenancy variables, including the IVFFlat reindex fix."
sources:
  - https://docs.openwebui.com/reference/env-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure the vector store behind RAG, knowledge bases and memories. Covers `VECTOR_DB` choice plus ChromaDB, PGVector and Qdrant settings (other stores are listed in the reference).

## Choose
`VECTOR_DB` options: `chroma` (default), `elasticsearch`, `mariadb-vector`, `milvus`, `opengauss`, `opensearch`, `pgvector`, `qdrant`, `pinecone`, `s3vector`, `oracle23ai`, `weaviate`, `valkey`. The slim image defaults to `pgvector` (`USE_SLIM_DOCKER`). Only PGVector and ChromaDB are consistently maintained by the Open WebUI team; the rest are community-added. For `pgvector` install the extras: `pip install open-webui[all]`.

Default ChromaDB is an embedded `PersistentClient` on local SQLite files: single instance only. Several replicas crash it (`Child process died`). For replicas use a client-server store, or run Chroma as a server.

## ChromaDB over HTTP
Setting `CHROMA_HTTP_HOST` switches to `HttpClient`. Related: `CHROMA_HTTP_PORT` (default 8000), `CHROMA_HTTP_HEADERS` (comma-separated, for example `Authorization=Bearer <token>,User-Agent=OpenWebUI`), `CHROMA_HTTP_SSL` (default False), `CHROMA_CLIENT_AUTH_PROVIDER` (for example `chromadb.auth.basic_authn.BasicAuthClientProvider`), `CHROMA_CLIENT_AUTH_CREDENTIALS` (`username:password`), `CHROMA_TENANT`, `CHROMA_DATABASE`.

## PGVector
```bash
VECTOR_DB=pgvector
PGVECTOR_DB_URL=postgresql://user:pass@host:5432/db   # default: DATABASE_URL
PGVECTOR_INDEX_METHOD=hnsw
```
- If `PGVECTOR_DB_URL` is unset, vectors go into the main `DATABASE_URL` database, which must be PostgreSQL with the `vector` extension.
- `PGVECTOR_CREATE_EXTENSION=false` assumes the extension already exists and lets Open WebUI run as a non-superuser.
- `PGVECTOR_INITIALIZE_MAX_VECTOR_LENGTH` (default 1536); above 2000 dimensions set `PGVECTOR_USE_HALFVEC=True`.
- Index: `hnsw` (better query speed, more memory; `PGVECTOR_HNSW_M` 16, `PGVECTOR_HNSW_EF_CONSTRUCTION` 64) or `ivfflat` (`PGVECTOR_IVFFLAT_LISTS` 100; start near rows/1000 up to 1M rows, `sqrt(rows)` beyond).
- IVFFlat is only built once `document_chunk` holds 50 rows per list (5,000 at the default); until then searches are exact scans. An older instance whose index was built on an empty table loses recall; repair once with `REINDEX INDEX idx_document_chunk_vector;`.
- `PGVECTOR_ITERATIVE_SCAN` (`relaxed_order` default, `strict_order`, `off`) keeps walking the index when the collection filter discards rows; needs pgvector 0.8+, and `ivfflat` always uses `relaxed_order`.
- Pool: `PGVECTOR_POOL_SIZE` (SQLAlchemy default), `PGVECTOR_POOL_MAX_OVERFLOW` 0, `PGVECTOR_POOL_TIMEOUT` 30, `PGVECTOR_POOL_RECYCLE` 3600. `PGVECTOR_PGCRYPTO=True` requires `PGVECTOR_PGCRYPTO_KEY`.

## Qdrant (non-core integration)
`QDRANT_URI`, `QDRANT_API_KEY`, `QDRANT_ON_DISK` (default False), `QDRANT_PREFER_GRPC` (default False, port `QDRANT_GRPC_PORT` 6334; with a private-CA TLS server set `GRPC_DEFAULT_SSL_ROOTS_FILE_PATH`), `QDRANT_TIMEOUT` (default 5 seconds), `QDRANT_HNSW_M` (16), `QDRANT_COLLECTION_PREFIX` (default `open-webui`).
`ENABLE_QDRANT_MULTITENANCY_MODE` defaults True and should stay on. Turning it on strands collections made in the old pattern: remove the `open_webui-knowledge` (or `open_webui`) prefix collections with the Qdrant client, then Admin Settings > Documents > Reindex Knowledge and Memory Vectors. That reindex covers knowledge bases, their file vectors and memories; loose files and cached web search results stay in old collections.

## Gotchas
- Multitenancy routing depends on current collection naming; snapshot Qdrant and back up before every upgrade.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page reference/env-configuration (read the Vector Database, ChromaDB, PGVector and Qdrant sections, plus USE_SLIM_DOCKER): VECTOR_DB options and defaults, the multi-replica ChromaDB warning, every CHROMA_*, PGVECTOR_* and QDRANT_* variable named with its default, the IVFFlat 50-rows-per-list note and REINDEX repair, iterative scan options and pgvector 0.8 gate, and the multitenancy migration steps. Removed: the claim that changing VECTOR_DB does not move vectors (not stated by the page).
Method: documentation only; no commands were run.
