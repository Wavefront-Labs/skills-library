---
id: computing-software.ai-ml-engineering.litellm.litellm-proxy-config-model-list
name: litellm-proxy-config-model-list
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, config-yaml, model-list, litellm-params]
level: intro
status: docs-checked
description: "Define models in config.yaml with model_name aliases and litellm_params, then start the proxy with --config."
sources:
  - https://docs.litellm.ai/docs/proxy/quick_start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure models with a config file instead of CLI flags.

```
model_list:
  - model_name: gpt-6-luna # user-facing model alias
    litellm_params: # all params accepted by litellm.completion()
      model: azure/<your-deployment-name>
      api_base: <your-azure-api-endpoint>
      api_key: <your-azure-api-key>
  - model_name: gpt-6-luna
    litellm_params:
      model: azure/gpt-turbo-small-ca
      api_base: https://my-endpoint-canada-berri992.openai.azure.com/
      api_key: <your-azure-api-key>
  - model_name: vllm-model
    litellm_params:
      model: openai/<your-model-name>
      api_base: <your-vllm-api-base> # e.g. http://0.0.0.0:3000/v1
      api_key: <your-vllm-api-key|none>
```

Run it:

```
litellm --config your_config.yaml
```

`model_name` is what clients send as `model`. Giving two entries the same model_name makes them one model group; requests are load balanced between the deployments. `litellm_params` accepts everything `litellm.completion()` accepts, such as api_base and max_tokens.

Clients: any OpenAI-compatible SDK works by pointing its base URL at the proxy:

```
client = openai.OpenAI(api_key="anything", base_url="http://0.0.0.0:4000")
```

The Anthropic SDK also works with base_url set to the proxy and a LiteLLM virtual key as api_key.

Using the LiteLLM SDK against the proxy is not recommended: the proxy also uses the SDK, so the logic is duplicated and can lead to unexpected errors.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/quick_start (config.yaml and SDK sections) and docs.litellm.ai/docs/routing (same model_name load balancing comment)
