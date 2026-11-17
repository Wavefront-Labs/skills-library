---
id: computing-software.ai-ml-engineering.open-webui.scale-open-webui-to-multiple-replicas
name: scale-open-webui-to-multiple-replicas
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [scaling, postgresql, redis, multi-replica, vector-db, shared-storage]
level: advanced
status: docs-checked
description: "Move Open WebUI from one SQLite instance to several replicas with PostgreSQL, Redis, an external vector database and shared file storage, in order."
sources:
  - https://docs.openwebui.com/getting-started/advanced-topics/scaling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run more than one Open WebUI instance safely. Defaults are embedded SQLite, embedded ChromaDB, local file storage and one Uvicorn worker; each of those breaks with replicas, so replace them in the order below.

## Step 1: PostgreSQL
Set `DATABASE_URL=postgresql://...`. Size the pool per process: `DATABASE_POOL_SIZE=15` with `DATABASE_POOL_MAX_OVERFLOW=20`. Total connections are (size + overflow) x replicas and must stay under PostgreSQL `max_connections` (default 100). SQLite on network storage fails with "database is locked". Open WebUI does not migrate data between databases; plan the move yourself before production data lands in SQLite.

## Step 2: Redis
On every instance set `REDIS_URL` and `WEBSOCKET_MANAGER=redis`. Without Redis, sign-out does not revoke tokens (`JWT_EXPIRES_IN` defaults to 4 weeks) and live updates stay on the replica that produced them.

## Step 3: replicas, not workers
Keep `UVICORN_WORKERS=1` and scale replicas. Compose: `docker compose up -d --scale open-webui=3` with no fixed host port mapping. Optional tuning: `ENABLE_COMPRESSION_MIDDLEWARE=false`, `UVICORN_WS_PER_MESSAGE_DEFLATE=false`, `WEBSOCKET_HEARTBEAT_INTERVAL=60`, `REDIS_RESPONSE_STREAM_TTL` (default 3600), `WEBSOCKET_REDIS_ROOM_CHANNELS=True` (all instances must match), `AIOHTTP_CLIENT_ASYNC_DNS_RESOLVER=True`, `ENABLE_ORJSON`. At the proxy, cache `location ^~ /_app/immutable/`, but leave the HTML shell and `/_app/version.json` uncached.

## Step 4: external vector database
The default embedded ChromaDB crashes multi-process ("Child process died"). Set `VECTOR_DB` to `pgvector` (`PGVECTOR_DB_URL`), `mariadb-vector`, `milvus` (`MILVUS_URI`), `qdrant` (`QDRANT_URI`), `pinecone`, or ChromaDB over HTTP (`CHROMA_HTTP_HOST` and `CHROMA_HTTP_PORT`). Qdrant multitenancy is on by default; Milvus multitenancy is off by default.

## Step 5: shared file storage
Use a shared filesystem (Kubernetes needs RWX) or S3, GCS or Azure via `STORAGE_PROVIDER`. With object storage, uploads and reads still use local disk under `DATA_DIR/uploads`; `STORAGE_LOCAL_CACHE=false` removes local copies of cloud-backed files after processing. Changing `STORAGE_PROVIDER` does not migrate existing files.

## Step 6 and 7
Offload extraction with `CONTENT_EXTRACTION_ENGINE=tika` plus `TIKA_SERVER_URL`, and embeddings with `RAG_EMBEDDING_ENGINE=openai` or `ollama`. Add observability: `ENABLE_OTEL=true`, `ENABLE_OTEL_TRACES=true`, `ENABLE_OTEL_METRICS=true` and `OTEL_EXPORTER_OTLP_ENDPOINT`.

## Minimum env for every replica
- `WEBUI_SECRET_KEY` identical everywhere.
- `ENABLE_DB_MIGRATIONS=false` on all but one instance.
- `THREAD_POOL_SIZE=2000` (default limit is 40).
- `ENABLE_CHAT_RESPONSE_STREAM_INPLACE_APPEND=True`.

## Security items
`ENABLE_PROFILE_IMAGE_URL_FORWARDING=false`, `ENABLE_OAUTH_ID_TOKEN_COOKIE=false`, set `OAUTH_SESSION_TOKEN_ENCRYPTION_KEY`, and lower `JWT_EXPIRES_IN`.

## Gotchas
- SQLite is fine for one replica on a local SSD/NVMe; skip Step 1 there.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: getting-started/advanced-topics/scaling (read in full). Removed: references to sibling skills that do not exist; replaced them with the page's own OpenTelemetry variables and local-cache behaviour.
Method: documentation only; no commands were run.
