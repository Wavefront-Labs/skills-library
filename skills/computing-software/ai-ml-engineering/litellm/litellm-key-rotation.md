---
id: computing-software.ai-ml-engineering.litellm.litellm-key-rotation
name: litellm-key-rotation
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, key-regenerate, auto-rotate, rotation-interval]
level: advanced
status: docs-checked
description: "Rotate virtual keys manually with /key/regenerate and a grace period, or automatically with auto_rotate. Enterprise feature."
sources:
  - https://docs.litellm.ai/docs/proxy/virtual_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Key rotation is marked an Enterprise feature on the docs page (it needs a LiteLLM Enterprise license).

Manual rotation (optionally updating parameters):

```
curl 'http://localhost:4000/key/sk-<virtual-key>/regenerate' \
  -X POST \
  -H "Authorization: Bearer $LITELLM_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"max_budget": 100, "models": ["gpt-6.1-sol"], "grace_period": "48h"}'
```

`grace_period` (such as "24h", "2d", "1w") keeps the old key valid alongside the new one until it elapses, for cutover without downtime. Omitted or empty means immediate revoke.

Scheduled rotation needs a database. Enable the worker and create keys with `auto_rotate`:

```
export LITELLM_KEY_ROTATION_ENABLED=true
export LITELLM_KEY_ROTATION_CHECK_INTERVAL_SECONDS=3600
export LITELLM_KEY_ROTATION_GRACE_PERIOD=48h
```

```
curl 'http://0.0.0.0:4000/key/generate' \
  -H 'Authorization: Bearer <your-master-key>' \
  -H 'Content-Type: application/json' \
  -d '{"models": ["gpt-6.1-sol"], "auto_rotate": true, "rotation_interval": "30d"}'
```

Defaults: LITELLM_KEY_ROTATION_ENABLED false; check interval 86400 seconds; grace period empty (immediate revoke).

How it works: next rotation = now + rotation_interval, stored in the database. A background job checks for keys past due, regenerates them, invalidates the old string and recalculates. Valid intervals use s, m, h or d suffixes (30s, 30m, 30h, 30d, 90d). Enable on an existing key via /key/update with `auto_rotate` and `rotation_interval`.

## Checked

2026-11-03. Confirmed on the virtual keys page (docs.litellm.ai/docs/proxy/virtual_keys): the /key/{key}/regenerate call, grace_period, the LITELLM_KEY_ROTATION_* variables and defaults (false, 86400, empty), auto_rotate, rotation_interval formats and the Enterprise marking. Reworded the licence line to what the page states.

Method: documentation only; no commands were run.
