---
id: computing-software.ai-ml-engineering.litellm.litellm-region-and-vision-filtering
name: litellm-region-and-vision-filtering
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, region-name, supports-vision, pre-call-checks]
level: advanced
status: docs-checked
description: "Filter deployments by region (EU) or by text-only status before a call using enable_pre_call_checks."
sources:
  - https://docs.litellm.ai/docs/proxy/reliability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Region filtering needs `router_settings.enable_pre_call_checks: true`; the docs say vision filtering runs by default under every routing strategy.

Region filtering: set `region_name` on the deployment.

```
router_settings:
  enable_pre_call_checks: true
model_list:
- model_name: gpt-6-luna
  litellm_params:
    model: azure/chatgpt-v-2
    api_base: os.environ/AZURE_API_BASE
    api_key: os.environ/AZURE_API_KEY
    api_version: "2023-07-01-preview"
    region_name: "eu"
- model_name: gpt-6-luna
  litellm_params:
    model: gpt-6-luna
    api_key: os.environ/OPENAI_API_KEY
```

LiteLLM can infer `region_name` automatically for Vertex AI, Bedrock and IBM WatsonxAI from your litellm params. For Azure, set `litellm.enable_preview = True`.

Verify which deployment served a request with the response header `x-litellm-model-api-base`.

Vision filtering: before a call, LiteLLM removes deployments declared text-only from the candidates for a request that carries an image (an image_url part in /v1/chat/completions, an input image in /v1/responses).

A deployment is text-only when `model_info.supports_vision: false` is set, or when that key is unset and the model catalog says supports_vision false for `model_info.base_model`, then `litellm_params.base_model`, then the model name.

```
  - model_name: mixed
    litellm_params:
      model: hosted_vllm/my-text-only-model
      api_base: os.environ/TEXT_API_BASE
    model_info:
      supports_vision: false
```

An image request then always lands on the vision-capable deployment (`x-litellm-model-id` names it), while plain text requests can land on any.

## Checked

2026-11-03. Confirmed on the reliability page (docs.litellm.ai/docs/proxy/reliability): enable_pre_call_checks, region_name, region inference for Vertex AI, Bedrock and WatsonxAI, litellm.enable_preview for Azure, x-litellm-model-api-base, the vision filter rules with model_info.supports_vision, and x-litellm-model-id. Reworded the opening line: vision filtering is documented as running by default.

Method: documentation only; no commands were run.
