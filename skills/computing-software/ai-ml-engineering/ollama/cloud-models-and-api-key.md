---
id: computing-software.ai-ml-engineering.ollama.cloud-models-and-api-key
name: cloud-models-and-api-key
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [cloud-models, api-key, retirements, data-handling, cloudmodels]
level: practitioner
status: docs-checked
description: "Use Ollama cloud models from the app, CLI or API: naming, listing, usage page, retirements and data handling."
sources:
  - https://docs.ollama.com/cloud.md
  - https://docs.ollama.com/quickstart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run models in Ollama's cloud without downloading them.

API route: create a key at ollama.com/settings/keys, `export OLLAMA_API_KEY="your_api_key"`, and call `https://ollama.com/api/chat` with a bearer header and a cloud model such as `gemma4:31b`. Read the answer from `message.content`. OpenAI and Anthropic clients are supported too, each as a subset of the original API. No Ollama installation is required.

App or CLI route: download Ollama, run `ollama` and follow the setup prompts to sign in. For coding agents run `ollama launch claude`, `ollama launch codex` (install Codex CLI first) or `ollama launch opencode`.

Naming: list cloud models with `curl https://ollama.com/api/tags`. For API requests to ollama.com use the returned name (such as `gemma4:31b`). In the Ollama app or CLI use `gemma4:cloud`. Cloud models need no download.

Plans and usage: check usage at ollama.com/settings/usage and compare plans at ollama.com/pricing. Usage settings show upcoming retirements for models you recently used; switch before the date. Downloaded local models are not affected.

Data handling: Ollama processes cloud prompts and responses to answer requests and says it does not use them to train models (see its privacy policy). To use only local models, the page points to the FAQ entry on disabling cloud features.

## Checked

Method: 2026-11-08 read cloud.md in full and the quickstart's cloud and launch sections. Removed unsupported claims (OLLAMA_NO_CLOUD=1 value, cloud structured-output limitation, full-context default).
