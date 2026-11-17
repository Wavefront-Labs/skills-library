---
id: computing-software.ai-ml-engineering.litellm.litellm-fallback-management-api
name: litellm-fallback-management-api
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, fallback-endpoint, store-model-in-db, context-window]
level: practitioner
status: docs-checked
description: "Create, read and delete model fallbacks with the dedicated /fallback endpoints instead of /config/update."
sources:
  - https://docs.litellm.ai/docs/proxy/fallback_management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: set `STORE_MODEL_IN_DB=True`, and the models must already exist in the router.

Create or update:

```
curl -X POST http://localhost:4000/fallback \
  -H "Authorization: Bearer $LITELLM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-6-luna",
    "fallback_models": ["gpt-6.1-sol", "claude-sonnet-5"],
    "fallback_type": "general"
  }'
```

`fallback_type` is optional: `general` (default, any error), `context_window` (context window exceeded) or `content_policy` (content policy violations).

Read and delete:

```
GET    /fallback/{model}?fallback_type=general
DELETE /fallback/{model}?fallback_type=general
```

Validation: the primary model must exist in the router; all fallback models must exist; no model can be its own fallback; no duplicates; the database must be enabled.

Errors: 400 for invalid fallback models (lists `available_models`), 404 when the model is not in the router, 500 when the router is not initialised.

Behaviour:

- Fallbacks fire after the configured retries fail.
- They are tried in the order given, up to the router's `max_fallbacks`.
- Changes take effect immediately and persist to the database.

Benefit over /config/update: it only modifies fallback configuration, so it cannot accidentally change other settings.

## Checked

Method: docs-checked 2026-11-09 against the full LiteLLM Fallback Management (proxy/fallback_management) page.
