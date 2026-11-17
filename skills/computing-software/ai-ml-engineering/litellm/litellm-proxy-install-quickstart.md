---
id: computing-software.ai-ml-engineering.litellm.litellm-proxy-install-quickstart
name: litellm-proxy-install-quickstart
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, proxy, install, quickstart]
level: intro
status: docs-checked
description: "Install the LiteLLM proxy with uv, start it from the CLI for one model, and test it with litellm --test."
sources:
  - https://docs.litellm.ai/docs/proxy/quick_start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run the LiteLLM proxy (LLM gateway) on port 4000.

Install:

```
uv tool install 'litellm[proxy]'
```

LiteLLM 1.84.0 and newer require Python 3.10 or higher. `uv tool install` provisions a compatible Python automatically. A bare `pip install 'litellm[proxy]'` does not: on an older interpreter pip silently resolves down to the last release whose requires-python allows it.

Start with one model from the CLI (provider keys are read from environment variables such as OPENAI_API_KEY or ANTHROPIC_API_KEY):

```
litellm --model huggingface/bigcode/starcoder
# INFO: Proxy running on http://0.0.0.0:4000
```

Test from a new shell (needs openai v1.0.0+):

```
litellm --test
```

Provider examples from the docs: `litellm --model azure/my-deployment-name` with AZURE_API_KEY and AZURE_API_BASE set; `litellm --model openai/<name> --api_base <url>` for any OpenAI-compatible endpoint; `litellm --model ollama/<name>`.

Core endpoints: POST /chat/completions, POST /completions, POST /embeddings, GET /models, POST /key/generate.

The commands on this page run without a database. To create virtual keys, track spend or use the Admin UI, add `database_url` under general_settings in config.yaml.

## Checked

2026-11-03. Confirmed on the proxy quick start page (docs.litellm.ai/docs/proxy/quick_start): uv tool install, the Python 3.10 floor for 1.84.0 and newer, litellm --model huggingface/bigcode/starcoder, litellm --test, openai v1.0.0+, the azure, openai/ with --api_base and ollama examples, the endpoint list and the database_url note. Removed the vllm/<name> example, which the page does not show.

Method: documentation only; no commands were run.
