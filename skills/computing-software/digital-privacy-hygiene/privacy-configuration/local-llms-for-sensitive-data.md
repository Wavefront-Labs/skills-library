---
id: computing-software.digital-privacy-hygiene.privacy-configuration.local-llms-for-sensitive-data
name: local-llms-for-sensitive-data
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, local-llm-for-sensitive-data, ai-privacy, ollama, offline-ai]
level: practitioner
status: docs-checked
description: "Run an AI model locally with Ollama, LM Studio or llama.cpp for sensitive documents, size hardware, confirm it stays offline, and pick safe model files."
sources:
  - "https://github.com/ollama/ollama"
  - "https://docs.ollama.com/faq"
  - "https://lmstudio.ai/"
  - "https://github.com/ggml-org/llama.cpp"
  - "https://huggingface.co/docs/hub/security-pickle"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running local models for sensitive work

**Goal:** summarise or draft from confidential material (medical, legal, client files) without sending it to a cloud
AI.

## Tools
| Tool | Style |
|---|---|
| Ollama | CLI and local API; `ollama run <model>` |
| LM Studio | Desktop GUI, model browser, local server |
| llama.cpp | Low-level engine (GGUF models) |
| Jan, GPT4All | Open-source desktop chat apps |

## Hardware rule of thumb
Model size must fit in RAM or GPU VRAM; check the model's listed download size in the tool and leave headroom for
the context window. Smaller or more heavily quantised models need less memory but lose accuracy.

## Keep it local
- Ollama binds `127.0.0.1` port `11434` by default and the bind address is changed with the `OLLAMA_HOST` environment
  variable; don't set it to `0.0.0.0` on untrusted networks, as that exposes the API.
- Ollama also offers cloud-hosted models, which process your prompts on its servers. Use only models that run locally
  for confidential material.
- Check settings for telemetry/analytics and turn them off; test by disconnecting the network and confirming it still
  works.
- Chat histories may be kept on disk by the app; use full-disk encryption and delete sessions with sensitive content.

## Model files
- Download from the official library or well-known publishers on Hugging Face.
- Prefer **GGUF** or **safetensors**; avoid pickle-based `.bin`/`.pt` files from unknown sources, which can execute code
  when loaded.

## Limits
Smaller local models are less accurate; verify outputs, especially on legal or medical facts. Plugins that browse the
web or call tools reintroduce network exposure.

## Checked
2026-11-01. Confirmed in the Ollama FAQ: default bind 127.0.0.1:11434, `OLLAMA_HOST` setting, local prompts not seen by
Ollama, cloud-hosted models process prompts. Confirmed in the Hugging Face pickle security page: pickled `.bin`/`.pt`
files are the risk. Removed unconfirmed RAM figures, scanning claim and plain-file history claim. Telemetry settings
and the offline test are practical advice, not documented claims.
Method: documentation only; no commands were run.
