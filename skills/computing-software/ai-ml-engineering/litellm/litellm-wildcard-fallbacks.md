---
id: computing-software.ai-ml-engineering.litellm.litellm-wildcard-fallbacks
name: litellm-wildcard-fallbacks
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, wildcard-fallbacks, provider-prefix, fallbacks]
level: advanced
status: docs-checked
description: "Set fallbacks for wildcard models like azure/* and provider-prefixed keys for bare model names such as claude-sonnet-5."
sources:
  - https://docs.litellm.ai/docs/proxy/reliability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define fallbacks for wildcard model entries, including provider-prefixed keys and a catch-all `*` key.
Wildcard targets:

```
model_list:
  - model_name: "gpt-6.1-sol"
    litellm_params:
      model: "openai/gpt-6.1-sol"
      api_key: os.environ/OPENAI_API_KEY
  - model_name: "azure/*"
    litellm_params:
      model: "azure/*"
      api_key: os.environ/AZURE_API_KEY
      api_base: os.environ/AZURE_API_BASE
litellm_settings:
  fallbacks: [{"gpt-6.1-sol": ["azure/gpt-6.1-sol"]}]
```

Provider-prefixed keys: a request for a bare model name such as `claude-sonnet-5` (the form Claude Code sends) is served by the `anthropic/*` deployment, and the fallback lookup matches it against a key written the way that wildcard is, `anthropic/claude-sonnet-5`.

```
model_list:
  - model_name: "anthropic/*"
    litellm_params:
      model: "anthropic/*"
      api_key: os.environ/ANTHROPIC_API_KEY
  - model_name: "openai/gpt-6.1-sol"
    litellm_params:
      model: "openai/gpt-6.1-sol"
      api_key: os.environ/OPENAI_API_KEY
  - model_name: "gpt-6-luna"
    litellm_params:
      model: "openai/gpt-6-luna"
      api_key: os.environ/OPENAI_API_KEY
litellm_settings:
  fallbacks:
    - {"anthropic/claude-sonnet-5": ["openai/gpt-6.1-sol", "gpt-6-luna"]}
    - {"*": ["gpt-6-luna"]}
```

A request for claude-sonnet-5 failing on anthropic/* is retried on openai/gpt-6.1-sol and then gpt-6-luna. A request for any other bare name without a key of its own goes straight to the `*` entry.
Fallbacks are set under `litellm_settings` as a list of one-key dictionaries mapping a model name to its ordered fallback list.

## Checked

2026-11-03. Confirmed on the reliability page (docs.litellm.ai/docs/proxy/reliability): wildcard fallback targets, the provider-prefixed fallback keys section for bare model names, and fallbacks under litellm_settings. Removed a generic testing sentence.

Method: documentation only; no commands were run.
