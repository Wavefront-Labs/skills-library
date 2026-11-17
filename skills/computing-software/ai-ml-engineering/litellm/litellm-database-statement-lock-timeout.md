---
id: computing-software.ai-ml-engineering.litellm.litellm-database-statement-lock-timeout
name: litellm-database-statement-lock-timeout
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, database-statement-timeout, database-lock-timeout, postgres]
level: sme
status: docs-checked
description: "Bound the server-side runtime of LiteLLM Postgres statements and lock waits so slow writes cannot hold row locks."
sources:
  - https://docs.litellm.ai/docs/proxy/configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Problem: `database_connect_timeout` and `database_socket_timeout` bound the connection, but not a statement already running; a slow write can keep executing on the server after the Prisma client stopped waiting, holding its row locks.

Set the two Postgres-side bounds:

```
general_settings:
  database_statement_timeout: 60  # seconds; cancels any statement running longer
  database_lock_timeout: 15       # seconds; fails a statement waiting this long for a lock
```

LiteLLM delivers them through the libpq `options` parameter on DATABASE_URL (`options=-c statement_timeout=60000 -c lock_timeout=15000`), since Postgres has no Prisma URL parameter for them. A cancelled statement surfaces as SQLSTATE 57014.

Notes from the docs:

- Both are opt-in; leave unset and nothing changes.
- Keep `database_lock_timeout` well below `database_statement_timeout`, so a write blocked behind another transaction's lock fails fast instead of consuming the whole statement budget.
- Neither is applied to DIRECT_URL, which Prisma uses for migrations; migrations legitimately run long and are never cancelled by these settings.
- An `options` value pinned on DATABASE_URL yourself is preserved, and a setting pinned there wins over the configured one. `database_extra_connection_params` wins over both.
- They scope the bounds to LiteLLM's own connections instead of every client of that database, unlike server or RDS parameter-group settings.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/configs (Bounding Statement and Lock Time section)
