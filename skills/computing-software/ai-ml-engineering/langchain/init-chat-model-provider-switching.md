---
id: computing-software.ai-ml-engineering.langchain.init-chat-model-provider-switching
name: init-chat-model-provider-switching
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, init-chat-model, provider-switching, chat-models, configurable-model]
level: practitioner
status: docs-checked
description: "Use init_chat_model to build chat models from provider strings, make the model runtime-configurable, and avoid the configurable_fields=any trap."
sources:
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/chat_models_universal_init.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/master/libs/langchain_v1/langchain/chat_models/base.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# init_chat_model and provider switching

**Goal:** select a chat model by string (config file, env var, per request) without importing each integration in app code.

## Fixed model
```python
from langchain.chat_models import init_chat_model
llm = init_chat_model("openai:gpt-5.5", temperature=0)
alt = init_chat_model("claude-opus-4-7", model_provider="anthropic")
```
- `provider:model` and `model` + `model_provider=` are equivalent. The docstring prefers the prefix form.
- A bare model name is inferred best-effort by prefix (`gpt-`, `o1`, `o3` -> openai; `claude` -> anthropic; `gemini` -> google_vertexai, with a DeprecationWarning that the default will change to google_genai). Inference is "not guaranteed", so prefer the prefixed form.
- Prefer pinned model IDs over moving aliases so behaviour does not drift if an alias is repointed.
- The integration package for the provider must be installed (for example `langchain-openai`, `langchain-anthropic`). A missing package raises ImportError naming the package to `pip install`; an unknown provider raises ValueError. Providers outside the built-in registry still work if their package is installed, but you must pass `model_provider` explicitly.
- Extra kwargs go to the provider class `__init__` (common: `temperature`, `max_tokens`, `timeout`, `max_retries`, `base_url`, `rate_limiter`).

## Runtime-configurable model
```python
configurable = init_chat_model(temperature=0)          # no model given
configurable.invoke("hi", config={"configurable": {"model": "gpt-5.5"}})

first = init_chat_model(
    "openai:gpt-5.5",
    configurable_fields=("model", "model_provider", "temperature", "max_tokens"),
    config_prefix="first",
)
first.invoke("hi", config={"configurable": {"first_model": "anthropic:claude-opus-4-7", "first_temperature": 0.5}})
```
- With no `model`, `configurable_fields` defaults to `("model", "model_provider")`. With a `model`, it defaults to None (fixed).
- `config_prefix` makes keys `{prefix}_{param}`, useful with several configurable models in one chain. An empty prefix uses bare names.
- `bind_tools` and `with_structured_output` can be called on the configurable object; they are queued and applied to whichever model is chosen at call time.
- Security: `configurable_fields="any"` makes `api_key`, `base_url` and similar settable at runtime, which can redirect requests. Enumerate fields explicitly whenever config can come from untrusted callers.

## Verify
- [ ] Smoke test invokes every model string in config once at deploy.
- [ ] Switching provider in config needs no code change and passes the eval set within tolerance.

## Checked
Date: 2026-11-09.
- Confirmed in the init_chat_model source docstring (langchain_v1 chat_models/base.py) and the v0.3 universal-init how-to notebook: prefix form and model_provider equivalence, prefix inference table and gemini DeprecationWarning, ImportError and ValueError behaviour, configurable_fields defaults, config_prefix key format, queued bind_tools/with_structured_output, security note on "any", listed kwargs.
- Removed as unconfirmed: the "claude-sonnet-5-5" and "gpt-5" model strings (replaced by the docstring's examples), claims that Claude 5 and GPT reasoning models reject temperature/top_p, that Anthropic requires max_tokens, the thinking/reasoning provider kwargs, msg.text for content blocks, the ChatPromptTemplate section, and "ImportError at call time".
Method: documentation only; no commands were run.
