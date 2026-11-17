---
id: computing-software.systems-network-administration.frigate.frigate-generative-ai-providers
name: frigate-generative-ai-providers
category: computing-software
field: systems-network-administration
product: frigate
tags: [generative-ai, genai-providers, genai-roles, ollama, vision-model, object-descriptions, custom-prompts]
level: advanced
status: docs-checked
description: "Configure Frigate generative AI providers and roles, pick a vision model and generate tracked object descriptions with custom prompts."
sources: ["https://docs.frigate.video/configuration/genai/genai_config/", "https://docs.frigate.video/configuration/genai/genai_objects/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Generative AI providers and object descriptions

`genai` is a map of named providers (letters, numbers, hyphens and underscores; the name cannot be changed in the UI afterwards). Each has `provider`, `base_url`, `api key`, `model` and `roles`. Example: `my_provider` with `provider: ollama`, `base_url: http://localhost:11434`, a vision model such as `qwen3-vl:4b` and `roles: [descriptions, embeddings, chat]`. The name is used elsewhere, for example `semantic_search.model`.

Roles are `chat`, `descriptions`, `embeddings` and `transcribe`. A provider handles the first three by default; `transcribe` must be listed explicitly. Each role goes to exactly one provider.

Support: llama.cpp supports all four roles; Ollama supports descriptions, chat and embeddings; OpenAI, Azure OpenAI and Google Gemini support descriptions, chat and transcription. The model must also be capable: vision-capable for descriptions and chat, multimodal for embeddings. API keys may be pasted or stored in an environment variable prefixed `FRIGATE_`. Local models need a GPU; CPU inference is not recommended. Recommended local vision models include `qwen3-vl` and `gemma4`.

Object descriptions: Frigate sends the thumbnails of a tracked object to the provider at the end of its lifecycle (optionally earlier after significantly changed frames). By default all objects and zones get descriptions; restrict with `objects` and `required_zones`. `use_snapshot: True` sends the snapshot instead of detect-stream frames. Toggle live over MQTT at `frigate/<camera>/object_descriptions/set`.

Prompts: the default prompt asks the model to infer the intent or behaviour of the `{label}` across the sequence of images rather than describe appearance. Custom prompts can use `{label}`, `{sub_label}` and `{camera}` and be set globally or per object type. Descriptions feed semantic search and can be edited in Explore.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/genai/genai_config, docs.frigate.video/configuration/genai/genai_objects (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.
