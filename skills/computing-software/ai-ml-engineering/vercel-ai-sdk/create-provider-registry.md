---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.create-provider-registry
name: create-provider-registry
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [provider-management, createproviderregistry, separator, global-provider, registry]
level: practitioner
status: docs-checked
description: "Build a createProviderRegistry with several providers, resolve models by provider:model strings, change the separator, and set the global default provider."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/provider-management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reach multiple providers through one registry and plain string ids.

Setup (keys are the prefixes):

```ts
import { anthropic } from '@ai-sdk/anthropic';
import { openai } from '@ai-sdk/openai';
import { createProviderRegistry, gateway } from 'ai';

export const registry = createProviderRegistry({ gateway, anthropic, openai });
```

Resolve models (default separator is `:`):
- `registry.languageModel('openai:gpt-6-astra')`
- `registry.embeddingModel('openai:text-embedding-3-small')`
- `registry.imageModel('openai:dall-e-3')`
- `registry.videoModel('fal:luma-dream-machine/ray-2')` (used with `experimental_generateVideo`)
- `registry.decisionModel('provider:model')` (for `experimental_decide`; language and image middleware does not apply to decisions)
- `registry.files('openai')` and `registry.skills('anthropic')` return upload interfaces, available when the registered provider (usually a `customProvider` with `files: openai.files()` or `skills: anthropic.skills()`) has them. Example: `uploadFile({ api: registry.files('openai'), data, filename })` returns `providerReference`, which you pass as a file part `data` in a user message.

Custom separator: `createProviderRegistry({ gateway, anthropic, openai }, { separator: ' > ' })`, then `registry.languageModel('openai > gpt-6-astra')`.

Combine with aliases: register `anthropic: customProvider({ languageModels: { fast: anthropic('claude-haiku-5-5'), reasoning: wrapLanguageModel({...defaultSettingsMiddleware...}) }, fallbackProvider: anthropic })`, an OpenAI-compatible provider via `createOpenAICompatible({ name, apiKey: process.env.CUSTOM_API_KEY, baseURL })`, and a provider limited to named models (no fallback). Use `satisfies AnthropicLanguageModelOptions` to type-check provider options.

Global provider (alternative to a registry): model strings with no prefix resolve through the global provider, which defaults to the Vercel AI Gateway. Override once at startup: `globalThis.AI_SDK_DEFAULT_PROVIDER = openai;` then `model: 'gpt-6-astra'` uses OpenAI.

Note: the provider id in the model string is the key you registered in the object passed to `createProviderRegistry`.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
