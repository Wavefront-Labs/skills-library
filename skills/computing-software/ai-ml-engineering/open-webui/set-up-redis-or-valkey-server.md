---
id: computing-software.ai-ml-engineering.open-webui.set-up-redis-or-valkey-server
name: set-up-redis-or-valkey-server
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [redis-valkey, redis, valkey, noeviction, maxclients, websocket-manager]
level: advanced
status: docs-checked
description: "Run Redis or Valkey for Open WebUI with the server settings that prevent client exhaustion and key eviction, then connect via REDIS_URL and WEBSOCKET_MANAGER."
sources:
  - https://docs.openwebui.com/tutorials/integrations/redis
  - https://docs.openwebui.com/tutorials/integrations/valkey
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a Redis (or Valkey) server safe for Open WebUI's auth and websocket state. Redis is required as soon as more than one Open WebUI process runs (several Uvicorn workers or instances) and it is what makes sign-out revoke a token. (Community tutorials, not supported by the Open WebUI team; Valkey is not part of what Open WebUI tests.)

## Compose
```yml
services:
  redis:
    image: redis:7-alpine
    container_name: redis
    volumes:
      - redis-data:/data
    command: "redis-server --save 30 1 --appendonly yes --maxclients 10000 --timeout 1800 --maxmemory-policy noeviction"
    healthcheck:
      test: "[ $$(redis-cli ping) = 'PONG' ]"
      start_period: 5s
      interval: 1s
      timeout: 3s
      retries: 5
    restart: unless-stopped
    cap_drop: [ALL]
    cap_add: [SETGID, SETUID, DAC_OVERRIDE]
    networks:
      - openwebui-network
volumes:
  redis-data:
networks:
  openwebui-network:
    external: true
```
Create the network once: `docker network create openwebui-network`. For Valkey swap the image to `docker.io/valkey/valkey:8.0.1-alpine`, the command to `valkey-server ...` and `valkey-cli`. No `ports` entry is needed inside the Docker network.

## Why those flags
- `--maxclients 10000 --timeout 1800`: with `timeout 0` idle connections never close and pile up until "max number of clients reached" gives every user a 500 on login (after days or weeks). `timeout` only reaps idle TCP connections, not sessions or JWTs. Monitor with `redis-cli INFO clients | grep connected_clients`. Live fix: `redis-cli CONFIG SET maxclients 10000` and `CONFIG SET timeout 1800`, persist in config, restart Redis.
- `--maxmemory-policy noeviction`: Open WebUI stores TTL'd token-revocation keys (`{prefix}:auth:token:<jti>:revoked`), locks and persistent websocket pools (`session_pool`, `usage_pool`). An `allkeys-*` policy can silently un-revoke signed-out tokens. If you must cap memory with eviction use only `volatile-ttl` or `volatile-lru`; better, set `maxmemory 512mb` with `noeviction` and alert on usage. Never run `FLUSHDB`/`FLUSHALL` on a live instance.
- Persistence: `--save 30 1` alone can lose up to 30 minutes on a crash; also use `appendonly yes` and `appendfsync everysec`.

## Pub/Sub buffer limits
With `WEBSOCKET_MANAGER=redis`, large Socket.IO payloads can disconnect Pub/Sub clients (logs: "Cannot publish to redis... retrying", `redis.exceptions.TimeoutError`). Check `redis-cli INFO stats | grep client_output_buffer_limit_disconnections`, `redis-cli SLOWLOG GET 50`, `redis-cli CONFIG GET client-output-buffer-limit`; raise with `client-output-buffer-limit normal 0 0 0 replica 268435456 67108864 60 pubsub 1073741824 268435456 180`.

## Connect Open WebUI
```bash
REDIS_URL="redis://redis:6379/0"      # Valkey too: scheme stays redis://
WEBSOCKET_MANAGER="redis"
```
Use the container name, never `127.0.0.1` or `localhost` from another container. `valkey://` / `VALKEY_URL` belongs to the unrelated Valkey vector database (`VECTOR_DB=valkey`).

## Verify
`docker exec -it redis redis-cli -p 6379 ping` returns `PONG`; `docker logs open-webui 2>&1 | grep -i redis`; with `GLOBAL_LOG_LEVEL=DEBUG` look for "Using Redis to manage websockets."; `redis-cli --scan --pattern "open-webui*"` shows `open-webui:session_pool`, `open-webui:usage_pool`, `open-webui:ratelimit:*`, `open-webui:auth:token:*:revoked`. `/ready` returns 503 while Redis does not answer.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: tutorials/integrations/redis and valkey. Nothing removed.
Method: documentation only; no commands were run.
