---
id: computing-software.ai-ml-engineering.open-webui.setup-openai-azure-litellm-image-generation
name: setup-openai-azure-litellm-image-generation
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, image-generation, openai, azure-openai, litellm, gpt-image]
level: practitioner
status: docs-checked
description: "Set up OpenAI-style image generation in Open WebUI for OpenAI, Azure OpenAI or a LiteLLM proxy, with model sizes and the Azure base URL and API version rules."
sources:
  - https://docs.openwebui.com/features/chat-conversations/image-generation-and-editing/openai
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configure OpenAI, Azure OpenAI or LiteLLM image generation

Goal: use any OpenAI-compatible image API from Settings > Admin > Images (community guide). All three variants use the engine `Default (Open AI)`.

## OpenAI
Enter your OpenAI API key and pick a model; allowed sizes depend on the model:
- DALL-E 2: `256x256`, `512x512`, `1024x1024`
- DALL-E 3: `1024x1024`, `1792x1024`, `1024x1792`
- GPT-Image (`gpt-image-2` is current, also `gpt-image-1`): `auto`, `1024x1024`, `1536x1024`, `1024x1536`

## Azure OpenAI
1. Engine `Default (Open AI)`.
2. API Base URL: `https://<instance-id>.cognitiveservices.azure.com/openai/deployments/<model>/` (or `https://<endpoint>.openai.azure.com/openai/deployments/<model>/`). If you copy the deployment Target URI, delete everything after the model name, e.g. `.../deployments/gpt-image-1/images/generations?api-version=...` becomes `.../deployments/gpt-image-1/`. Keep the trailing slash.
3. Set the API version from Azure AI Foundry, and the Azure API key.
4. For `gpt-image-1.5`: model `gpt-image-1.5`, size `1024x1024`, API version `2025-04-01-preview` or later. The error `Unknown parameter: 'response_format'` means the API version is too old.

## LiteLLM proxy
Engine `Default (Open AI)`, API Base URL `https://<your-litellm-url>:<port>/v1`, your LiteLLM key, leave API version blank, enter the image model name exactly as in the LiteLLM config, and choose a size valid for that model. The connection details are visible under Settings > Admin > AI > Connections (OpenAI API connection).

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/chat-conversations/image-generation-and-editing/openai (read in full). Removed: the Gotchas section (usual-cause and trigger claims) the page does not make.
Method: documentation only; no commands were run.
