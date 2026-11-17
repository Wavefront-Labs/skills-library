---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.choose-ai-sdk-provider-and-model
name: choose-ai-sdk-provider-and-model
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [providers-and-models, providers, model-capabilities, openai-compatible, self-hosted]
level: intro
status: docs-checked
description: "Pick an AI SDK provider package and a model whose capabilities (image input, object generation, tool use, tool streaming) match the feature you are building."
sources:
  - https://ai-sdk.dev/docs/foundations/providers-and-models
  - https://ai-sdk.dev/docs/foundations/tools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: choose the provider package and model for an AI SDK call and confirm the model supports the features you plan to use.

## How the SDK abstracts providers
AI SDK Core talks to every model through a standardized language model specification (published as an open-source package), so switching provider keeps the same `generateText` / `streamText` API. Each provider is its own npm package, for example `@ai-sdk/openai`, `@ai-sdk/anthropic`, `@ai-sdk/google`, `@ai-sdk/google-vertex`, `@ai-sdk/azure`, `@ai-sdk/amazon-bedrock`, `@ai-sdk/mistral`, `@ai-sdk/xai`, `@ai-sdk/groq`, `@ai-sdk/deepseek`, `@ai-sdk/cerebras`.

## Steps
1. Decide which capabilities the feature needs: image input, object generation (structured output), tool usage, tool streaming.
2. Look the model up in the Model Capabilities table of the providers page. It has one column per capability, ticked or crossed per model. Example rows: Anthropic `claude-sonnet-5-5` supports all four; OpenAI `gpt-5-chat-latest` supports image input but not object generation, tool usage or tool streaming; Groq `llama-3.3-70b-versatile` has no image input but supports the other three. The table is explicitly not exhaustive; check the provider page for other models.
3. Install the provider package and pass the model, e.g. `anthropic('claude-sonnet-5-5')`. The tools page also passes plain model strings such as `'openai/gpt-6-luna'` or `'anthropic/claude-haiku-5.5'` to `generateText`.
4. Self-hosting: the docs list Ollama (community provider `ollama-ai-provider`), LM Studio and Heroku (via the OpenAI Compatible provider), Baseten (`@ai-sdk/baseten`) and Browser AI. Any server speaking the OpenAI specification works through the OpenAI Compatible provider.
5. Non-listed vendors: community providers exist for OpenRouter (`@openrouter/ai-sdk-provider`), Cloudflare Workers AI (`workers-ai-provider`), Portkey and others; you can also build a custom provider against the published specification.

## Gotchas
- Capabilities differ per model (see the table columns); check them before relying on image input, object generation or tool use.
- Speech, transcription and similar providers (ElevenLabs, Deepgram, AssemblyAI, Rev.ai, Gladia, Hume) appear as their own packages in the same provider list; check each provider page for the model types it offers.
- Model ids change quickly; verify the id in the provider page rather than copying from an old project.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the AI Gateway claim for plain model strings, the multi-modal rejection gotcha and "not language models"; added the foundations/tools page for the plain-string examples.

Method: documentation only; no commands were run.
