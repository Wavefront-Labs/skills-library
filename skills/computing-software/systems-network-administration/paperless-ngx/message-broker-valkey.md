---
id: computing-software.systems-network-administration.paperless-ngx.message-broker-valkey
name: message-broker-valkey
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, redis, valkey, message-broker, paperless-redis, celery]
level: practitioner
status: docs-checked
description: "Configure the Redis-compatible broker Paperless-ngx needs: URL forms, password, database index, key prefix, and switching between Valkey and Redis."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/faq/"
  - "https://docs.paperless-ngx.com/troubleshooting/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message broker

Paperless needs a Redis-compatible broker for scheduled tasks (email fetching, index optimization, training the automatic matcher) and for asynchronous document task processing. Any broker speaking the Redis protocol works: Valkey (the default in the bundled compose files), Redis, or wire-compatible brokers such as Microsoft's Garnet.

## PAPERLESS_REDIS
Defaults to `redis://localhost:6379`. Forms:
- With credentials: `redis://<username>:<password>@<host>:<port>`
- With only `requirepass`: `redis://:<password>@<host>:<port>`
- With a database index: `redis://<username>:<password>@<host>:<port>/<DBIndex>`

## PAPERLESS_REDIS_PREFIX
Prefix for keys and channels. Set a different prefix per instance when several Paperless instances share one broker.

## Switching implementations
An existing install can change broker implementation in place: point `PAPERLESS_REDIS` at the new instance and reuse the same data volume.

## Troubleshooting
If documents are added but never processed, check that the broker is reachable and that the task processor is running. In Docker this is automatic; on bare metal start it with:
```bash
celery --app paperless worker
```
The configuration page advises securing your broker instance and links to the Valkey security guide.

## Checked
2026-11-04. Compared with Message Broker settings in configuration, Which message broker should I use in the FAQ, and the broker and task processor checks in troubleshooting (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: Redis-compatible requirement, Valkey default, Garnet, URL forms, default URL, prefix purpose, in-place switching, celery worker command. Reworded the purpose sentence and the closing security line to match the pages.

Method: documentation only; no commands were run.
