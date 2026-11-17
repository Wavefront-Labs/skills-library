---
id: computing-software.ai-ml-engineering.litellm.litellm-prod-spend-writes-and-logging
name: litellm-prod-spend-writes-and-logging
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, proxy-batch-write-at, disable-error-logs, json-logs]
level: practitioner
status: docs-checked
description: "Reduce database load and log noise in production: batch spend writes, skip error logs in the DB, JSON logs, request timeout."
sources:
  - https://docs.litellm.ai/docs/proxy/prod
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Batch spend writes: write spend updates every 60 seconds instead of on every request, since at production traffic per-request writes become a database hot spot.

```
general_settings:
  proxy_batch_write_at: 60
```

Above roughly 1000 requests per second also route these writes through Redis with the transaction buffer (see the Redis skill).

Keep error logs out of the database: LLM exceptions are written to the database by default and bloat the spend logs table under sustained provider errors.

```
general_settings:
  disable_error_logs: True
```

Send exceptions to your logging stack instead.

Request timeout: fail requests that hang instead of holding connections open. The default is 6000 seconds.

```
litellm_settings:
  request_timeout: 600
```

Production logging: turn off debug logging, emit JSON logs and silence FastAPI per-request info logs:

```
litellm_settings:
  set_verbose: False
  json_logs: true
```

```
export LITELLM_LOG="ERROR"
```

Config reload across pods: with `store_model_in_db: true`, each pod polls the database in a background job to pick up config added at runtime (models, credentials, guardrails, general settings). There is no cross-pod push.

```
general_settings:
  store_model_in_db: true
  proxy_config_reload_interval_seconds: 30
```

The value is read at startup, so a change applies once each pod restarts. The env var `PROXY_CONFIG_RELOAD_INTERVAL_SECONDS` also works.

## Checked

2026-11-03. Confirmed on the LiteLLM production page (docs.litellm.ai/docs/proxy/prod): proxy_batch_write_at 60, the 1000 requests per second Redis note, disable_error_logs, the 6000 second request_timeout default, set_verbose, json_logs, LITELLM_LOG, store_model_in_db with proxy_config_reload_interval_seconds and PROXY_CONFIG_RELOAD_INTERVAL_SECONDS.

Method: documentation only; no commands were run.
