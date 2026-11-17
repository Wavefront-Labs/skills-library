---
id: computing-software.ai-ml-engineering.litellm.litellm-credential-list
name: litellm-credential-list
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, credential-list, litellm-credential-name, secret-rotation]
level: advanced
status: docs-checked
description: "Define credentials once in credential_list and reference them from many models with litellm_credential_name."
sources:
  - https://docs.litellm.ai/docs/proxy/configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reduce duplicated keys and ease secret rotation.

```
model_list:
  - model_name: gpt-6.1-sol
    litellm_params:
      model: azure/gpt-6.1-sol
      litellm_credential_name: default_azure_credential

credential_list:
  - credential_name: default_azure_credential
    credential_values:
      api_key: os.environ/AZURE_API_KEY
      api_base: os.environ/AZURE_API_BASE
      api_version: "2023-05-15"
    credential_info:
      description: "Production credentials for EU region"
      custom_llm_provider: "azure"
```

Parameters:

- `credential_name`: unique identifier for the set.
- `credential_values`: key-value credentials/secrets; supports `os.environ/`.
- `credential_info`: user-provided information; no keys are required but the dictionary must exist.

Credential names are permanent: models and vector stores reference a credential by name, so a PATCH with a different `credential_name` returns 400. To relabel in the Admin UI set `display_name` (optional, not unique, max 255 characters; omit it on PATCH to keep it, send null to clear):

```
curl -X PATCH http://localhost:4000/credentials/default_azure_credential \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"display_name": "Azure EU (prod)", "credential_info": {}}'
```

Credentials in credential_list can only be changed in config.yaml: PATCH and DELETE on them return 405, and the UI disables Edit and Delete.

## Checked

2026-11-03. Confirmed on the LiteLLM proxy config page (docs.litellm.ai/docs/proxy/configs): credential_list, credential_name, credential_values, credential_info, permanent credential names (400), display_name (255 characters, null clears), and 405 for PATCH/DELETE on config-defined credentials.

Method: documentation only; no commands were run.
