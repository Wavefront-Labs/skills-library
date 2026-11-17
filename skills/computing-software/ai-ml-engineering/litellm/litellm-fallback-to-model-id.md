---
id: computing-software.ai-ml-engineering.litellm.litellm-fallback-to-model-id
name: litellm-fallback-to-model-id
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, fallbacks, model-info-id, cooldown-bypass]
level: advanced
status: docs-checked
description: "Fall back to one specific deployment by model_info.id, skipping its cooldown check, when a whole model group is cooled down."
sources:
  - https://docs.litellm.ai/docs/proxy/reliability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If all models in a group are in cooldown (for example rate limited), LiteLLM can fall back to a model by its specific id. This skips any cooldown check for the fallback model.

```
model_list:
  - model_name: gpt-6.1-sol
    litellm_params:
      model: openai/gpt-6.1-sol
    model_info:
      id: my-specific-model-id
  - model_name: gpt-6.1-sol
    litellm_params:
      model: azure/chatgpt-v-2
      api_base: os.environ/AZURE_API_BASE
      api_key: os.environ/AZURE_API_KEY
litellm_settings:
  fallbacks: [{"gpt-6.1-sol": ["my-specific-model-id"]}]
```

Notes:

- This only falls back to the deployment with that id. To fall back to another model group, use `fallbacks=[{"gpt-6.1-sol": ["anthropic-claude"]}]`.
- Test while the primary deployment is unavailable.

Verify: the response header `x-litellm-model-id: my-specific-model-id`.

Track which requests were served by a fallback: the proxy writes two keys into the `metadata` column of LiteLLM_SpendLogs:

- `attempted_fallbacks` (int): fallback attempts made; 0 means the requested model group served the request.
- `original_model_group` (str): the group the client originally requested.

```
SELECT model_group,
       metadata->>'attempted_fallbacks' AS attempted_fallbacks,
       metadata->>'original_model_group' AS original_model_group
FROM "LiteLLM_SpendLogs";
```

Both keys are set by the proxy and overwrite client-supplied values of the same name. Rows written before this feature read null.

## Checked

Method: docs-checked 2026-11-09 against the full LiteLLM Fallbacks (proxy/reliability) page, Fallback to Specific Model ID and Track Fallbacks in Spend Logs sections.
