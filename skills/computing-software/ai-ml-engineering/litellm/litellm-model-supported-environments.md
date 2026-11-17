---
id: computing-software.ai-ml-engineering.litellm.litellm-model-supported-environments
name: litellm-model-supported-environments
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, supported-environments, litellm-environment, model-info]
level: practitioner
status: docs-checked
description: "Expose a model only on production, staging or development proxies with LITELLM_ENVIRONMENT and model_info.supported_environments."
sources:
  - https://docs.litellm.ai/docs/proxy/configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose a different set of models per deployment stage from one config.yaml, selected by an environment variable on each proxy instance.
Goal: control which models a given proxy environment serves.

Supported environments: `production`, `staging`, `development`.

Step 1: set the environment variable on the proxy:

```
LITELLM_ENVIRONMENT="production"
```

Step 2: list the environments per model in `model_info.supported_environments`:

```
model_list:
 - model_name: gpt-6-luna
   litellm_params:
     model: openai/gpt-6-luna
     api_key: os.environ/OPENAI_API_KEY
   model_info:
     supported_environments: ["development", "production", "staging"]
 - model_name: gpt-6.1-sol
   litellm_params:
     model: openai/gpt-6.1-sol
     api_key: os.environ/OPENAI_API_KEY
   model_info:
     supported_environments: ["production", "staging"]
 - model_name: claude-sonnet-5
   litellm_params:
     model: anthropic/claude-sonnet-5
     api_key: os.environ/ANTHROPIC_API_KEY
   model_info:
     supported_environments: ["production"]
```

A proxy with LITELLM_ENVIRONMENT=development would then expose only gpt-6-luna; staging exposes the first two; production all three.

The value must be one of the three listed names.

`model_info` also carries other per-model metadata, such as `access_groups` and `custom_tokenizer`, as shown elsewhere on the config page.
Each proxy instance reads its own LITELLM_ENVIRONMENT value, so the same config.yaml file can be shared between production, staging and development deployments while the visible model list differs per stage.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/configs (supported environments section)
