---
id: computing-software.ai-ml-engineering.litellm.litellm-wildcard-default-models
name: litellm-wildcard-default-models
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, wildcard-model, default-models, model-list]
level: practitioner
status: docs-checked
description: "Expose all models of a provider without listing them by using a wildcard model_name entry in model_list."
sources:
  - https://docs.litellm.ai/docs/proxy/configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve every model of a provider without listing each one in model_list.
Goal: let clients call models you have not defined individually.

```
model_list:
  - model_name: "*"
    litellm_params:
      model: "*"
```

This works for ALL providers and needs the default provider credentials in the environment (.env). With it, clients can request models such as `claude-sonnet-5` or `claude-opus-5` without them being listed in config.yaml.

Provider-scoped wildcard with a key from the environment:

```
  - model_name: "*"
    litellm_params:
      model: openai/*
      api_key: os.environ/OPENAI_API_KEY
```

Multiple OpenAI organisations: one definition can cover models across several organisations by giving `organization` a list.

```
  - model_name: "*"
    litellm_params:
      model: openai/*
      api_key: os.environ/OPENAI_API_KEY
      organization:
       - org-1
       - org-2
       - org-3
```

LiteLLM automatically creates a separate deployment for each org. Confirm with:

```
curl --location 'http://0.0.0.0:4000/v1/model/info' \
--header 'Authorization: Bearer ${LITELLM_KEY}'
```

## Checked

2026-11-03. Confirmed on the LiteLLM proxy config page (docs.litellm.ai/docs/proxy/configs): the "*" wildcard entry, that it works for all providers with default credentials in .env, provider-scoped wildcards, an organization list creating a deployment per organisation, and the /v1/model/info check. Removed two unconfirmed closing sentences.

Method: documentation only; no commands were run.
