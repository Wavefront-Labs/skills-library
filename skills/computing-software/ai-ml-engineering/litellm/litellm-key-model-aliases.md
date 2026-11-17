---
id: computing-software.ai-ml-engineering.litellm.litellm-key-model-aliases
name: litellm-key-model-aliases
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, key-aliases, model-alias, upgrade-downgrade]
level: practitioner
status: docs-checked
description: "Map the model name a client sends to a different model group per virtual key to upgrade or downgrade requests."
sources:
  - https://docs.litellm.ai/docs/proxy/virtual_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a user asks for `gpt-6-luna` but you want their key to serve something else (a cheaper or newer model) without changing the client.

Step 1: define model groups in config.yaml:

```
model_list:
  - model_name: my-free-tier
    litellm_params:
        model: huggingface/HuggingFaceH4/zephyr-7b-beta
        api_base: http://0.0.0.0:8001
  - model_name: my-free-tier
    litellm_params:
        model: huggingface/HuggingFaceH4/zephyr-7b-beta
        api_base: http://0.0.0.0:8002
  - model_name: my-paid-tier
    litellm_params:
        model: gpt-6.1-sol
        api_key: my-api-key
```

Step 2: generate a key with an `aliases` map:

```
curl -X POST "https://0.0.0.0:4000/key/generate" \
-H "Authorization: Bearer <your-master-key>" \
-H "Content-Type: application/json" \
-d '{
	"models": ["my-free-tier"],
	"aliases": {"gpt-6-luna": "my-free-tier"},
	"duration": "30min"
}'
```

Step 3: the client calls the proxy with `"model": "gpt-6-luna"` and the key; the request is served by `my-free-tier`.

To upgrade or downgrade a user, change the alias mapping on the key. The docs' example also lists the target group (`my-free-tier`) in the key's `models`. The `/key/info` response shows the `aliases` that are set.

`duration` (for example "30min") sets the key's lifetime in the docs' example.

## Checked

Method: docs-checked 2026-11-09 against the LiteLLM Virtual Keys (proxy/virtual_keys) page, Model Aliases section and key info sample; trimmed the claim that the models list must include the target group.
