---
id: computing-software.ai-ml-engineering.litellm.litellm-env-var-references-in-config
name: litellm-env-var-references-in-config
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, os-environ, secrets, config-yaml]
level: intro
status: docs-checked
description: "Keep secrets out of config.yaml with the os.environ/<VAR> reference, which works for any config value."
sources:
  - https://docs.litellm.ai/docs/proxy/configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep secrets out of config.yaml by referencing environment variables.
Goal: avoid writing API keys in the config file.

Syntax: `os.environ/<YOUR-ENV-VAR>` runs `os.getenv("YOUR-ENV-VAR")`. It works for ANY value in config.yaml.

```
model_list:
  - model_name: gpt-4-team1
    litellm_params:
      model: azure/chatgpt-v-2
      api_base: https://openai-gpt-4-test-v-1.openai.azure.com/
      api_version: "2023-05-15"
      api_key: os.environ/AZURE_NORTH_AMERICA_API_KEY
```

Same pattern for the master key:

```
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

Setting `master_key` requires every call to the proxy to carry it, or a valid generated key, as `Authorization: Bearer $LITELLM_API_KEY`.

Per-deployment rate limits `rpm` and `tpm` can sit next to the key in litellm_params.

Alternatives for secrets:

- Centralised credentials with `credential_list` and `litellm_credential_name` (see the credential skill).
- A secret manager such as Azure Key Vault; the config page links to the "Using Secret Managers with LiteLLM Proxy" doc.

When running more than one proxy, put shared state such as load balancing counters in Redis via `router_settings: redis_host`, `redis_password`, `redis_port`.
Any config value can use the `os.environ/` prefix.

## Checked

2026-11-03. Confirmed on the LiteLLM proxy config page (docs.litellm.ai/docs/proxy/configs): the os.environ/ syntax working for any config value, master_key from the environment, requiring Authorization: Bearer when a master key is set, and the secret manager pointer.

Method: documentation only; no commands were run.
