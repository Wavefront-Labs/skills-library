---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.set-provider-options-at-call-message-and-part-level
name: set-provider-options-at-call-message-and-part-level
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [provider-options, prompts, prompt-caching, ai-gateway, type-safety]
level: practitioner
status: docs-checked
description: "Pass providerOptions at call, message or message-part level, namespace by provider, type them with satisfies, and combine gateway and provider options."
sources:
  - https://ai-sdk.dev/docs/foundations/provider-options
  - https://ai-sdk.dev/docs/foundations/prompts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: send provider-specific settings (reasoning, caching, image detail, routing) that go beyond the shared call settings.

## Where to put them
1. **Function call level** (use when you do not need granular control over where options apply): `providerOptions` on `generateText` / `streamText`.
   ```ts
   providerOptions: { openai: { reasoningEffort: 'low' } }
   ```
2. **Message level**: `providerOptions` on a message object, e.g. a cache-control breakpoint on a system message:
   ```ts
   instructions: {
     role: 'system',
     content: 'Cached system message',
     providerOptions: { anthropic: { cacheControl: { type: 'ephemeral' } } },
   }
   ```
3. **Message part level**: on a text or file part, e.g. `providerOptions: { openai: { imageDetail: 'low' } }`.

## Namespacing
Options are keyed by provider name (`openai`, `anthropic`). You can include several providers in one call; only the active provider's options are used.

## Type safety
Each provider exports an options type; use `satisfies` for autocomplete and typo detection:
```ts
import { openai, type OpenAILanguageModelResponsesOptions } from '@ai-sdk/openai';
providerOptions: { openai: { reasoningEffort: 'low' } satisfies OpenAILanguageModelResponsesOptions }
```
Anthropic exports `AnthropicLanguageModelOptions`; the gateway exports `GatewayProviderOptions` from `@ai-sdk/gateway`.

## With the AI Gateway
Use the underlying provider name as key, not `gateway`; the gateway forwards it. Gateway routing options go in a separate `gateway` key in the same object:
```ts
model: 'anthropic/claude-sonnet-4',
providerOptions: {
  gateway: { order: ['vertex', 'anthropic'] } satisfies GatewayProviderOptions,
  anthropic: { thinking: { type: 'enabled', budgetTokens: 12000 } } satisfies AnthropicLanguageModelOptions,
}
```

## Gotchas
- For reasoning effort prefer the portable top-level `reasoning` parameter; use provider options only for provider features such as exact token budgets.
- `UIMessage` objects from `useChat` do not support provider options; convert with `convertToModelMessages` before adding them.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Replaced the "default choice" label with the docs wording.

Method: documentation only; no commands were run.
