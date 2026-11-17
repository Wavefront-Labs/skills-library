---
id: computing-software.ai-ml-engineering.litellm.litellm-allow-requests-on-db-unavailable
name: litellm-allow-requests-on-db-unavailable
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, allow-requests-on-db-unavailable, graceful-degradation, readiness]
level: advanced
status: docs-checked
description: "Keep serving requests through a Postgres outage with allow_requests_on_db_unavailable, only on a private VPC."
sources:
  - https://docs.litellm.ai/docs/proxy/prod
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Warning: only enable this when LiteLLM runs on a VPC that cannot be accessed from the public internet.

```
general_settings:
  allow_requests_on_db_unavailable: True
```

Behaviour:

- Prisma connection errors (database engine unreachable, connection refused or reset, EngineConnectionError): request allowed, with a restricted INTERNAL_USER fallback identity.
- Prisma query errors (P2xxx, for example P2010): request blocked with a 401, because the database answered but the key cannot be verified (fail closed).
- Httpx errors: allowed.
- Pod startup: pods start even if the database is down.
- `/health/readiness`: always returns 200 OK so pods stay up.
- Budget or model errors when the database is reachable but the token is invalid, lacks access or is over budget: blocked.

During an outage, virtual keys already in the in-memory auth cache keep authenticating until `user_api_key_cache_ttl` expires (default 60 seconds; longer with `enable_redis_auth_cache`).

Related database TLS: to verify the server certificate against a provider CA (AWS RDS and similar) without a custom image:

```
export DATABASE_URL="postgresql://user:pass@host:5432/litellm?sslmode=verify-full&sslrootcert=/certs/global-bundle.pem"
```

LiteLLM rewrites these into the driver's params (sslmode=require, sslcert=<bundle>, sslaccept=strict) on DATABASE_URL, DIRECT_URL and DATABASE_URL_READ_REPLICA. This is separate from `SSL_CERT_FILE`, which only affects outbound HTTPS calls.

## Checked

2026-11-03. Confirmed on the LiteLLM production page (docs.litellm.ai/docs/proxy/prod): allow_requests_on_db_unavailable, the Prisma connection versus query error behaviour (INTERNAL_USER fallback, 401 for P2xxx), httpx errors, /health/readiness, user_api_key_cache_ttl default 60 seconds, enable_redis_auth_cache, and the sslmode verify-full rewrite for DATABASE_URL, DIRECT_URL and DATABASE_URL_READ_REPLICA versus SSL_CERT_FILE.

Method: documentation only; no commands were run.
