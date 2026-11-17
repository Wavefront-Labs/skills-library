---
id: computing-software.ai-ml-engineering.litellm.litellm-config-yaml-sections
name: litellm-config-yaml-sections
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, config-yaml, router-settings, general-settings]
level: intro
status: docs-checked
description: "The five top-level sections of the LiteLLM proxy config.yaml and how model_name maps to litellm_params.model."
sources:
  - https://docs.litellm.ai/docs/proxy/configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know where each setting goes.

- `model_list`: models on the server, with model-specific configs.
- `router_settings`: litellm Router settings, for example `routing_strategy`.
- `litellm_settings`: litellm module settings, for example `drop_params: True`, `set_verbose`, `success_callback`, cache.
- `general_settings`: server settings, for example `master_key`, `alerting`.
- `environment_variables`: env vars such as REDIS_HOST and REDIS_PORT.

The complete list of accepted keys is in the Swagger UI at `<your-proxy-url>/#/config.yaml`, for example http://0.0.0.0:4000/#/config.yaml.

Naming:

- `model_name`: the name the external client sends.
- `litellm_params.model`: the model string passed to `litellm.completion()`.

Several entries with the same `model_name` are load balanced:

```
model_list:
  - model_name: gpt-6.1-sol
    litellm_params:
      model: azure/gpt-6.1-sol-eu
      api_base: https://my-endpoint-europe-berri-992.openai.azure.com/
      api_key: "os.environ/AZURE_API_KEY_EU"
      rpm: 6
  - model_name: gpt-6.1-sol
    litellm_params:
      model: azure/gpt-6.1-sol-ca
      api_key: "os.environ/AZURE_API_KEY_CA"
      rpm: 6
```

Start with `litellm --config /path/to/config.yaml`. Look for the log line `LiteLLM: Proxy initialized with Config, Set models:` to confirm the config loaded.

The `openai/` prefix on `model` tells litellm the endpoint is OpenAI compatible, as for a vLLM server.

## Checked

2026-11-03. Confirmed on the LiteLLM proxy config page (docs.litellm.ai/docs/proxy/configs): the five top-level sections and their descriptions, the Swagger UI path /#/config.yaml, model_name versus litellm_params.model, same-name load balancing, and the Proxy initialized with Config log line, the openai/ prefix note.

Method: documentation only; no commands were run.
