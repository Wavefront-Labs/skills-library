---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.wrap-model-with-builtin-middleware
name: wrap-model-with-builtin-middleware
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [middleware, wraplanguagemodel, defaultsettingsmiddleware, extractreasoningmiddleware, extractjsonmiddleware, simulatestreamingmiddleware]
level: practitioner
status: docs-checked
description: "Apply built-in language model middleware with wrapLanguageModel: default settings and instructions, reasoning and JSON extraction, simulated streaming."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/middleware
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change a model's behavior once, then use the wrapped model anywhere (`generateText`, `streamText`, agents).

```ts
import { wrapLanguageModel, defaultSettingsMiddleware } from 'ai';

const model = wrapLanguageModel({
  model: yourModel,
  middleware: defaultSettingsMiddleware({
    settings: { temperature: 0.5, maxOutputTokens: 800, providerOptions: { openai: { store: false } } },
  }),
});
```

Multiple middlewares: `middleware: [first, second]` is applied as `first(second(yourModel))`.

Built-ins exported from `ai`:
- `defaultSettingsMiddleware({ settings })`: default call settings (see above).
- `defaultInstructionsMiddleware({ instructions: 'You are a concise technical assistant.' })`: adds instructions only when the call has no system message; call-level instructions win. `instructions` also takes a `SystemModelMessage` or array of them (for provider options). Any system message in the normalized prompt counts as call-level, so defaults are skipped; only enable `allowSystemInMessages` for trusted histories because a system message there can override the defaults.
- `extractReasoningMiddleware({ tagName: 'think' })`: pulls text between think tags into a `reasoning` property on the result. Option `startWithReasoning: true` prepends the tag for models that omit it at the start of the response (for example DeepSeek R1).
- `extractJsonMiddleware()`: strips markdown code fences so `Output.object({ schema })` parses for models that wrap JSON in fences. Custom formatting: `extractJsonMiddleware({ transform: text => text.replace(/^PREFIX/, '').replace(/SUFFIX$/, '') })`.
- `simulateStreamingMiddleware()`: gives non-streaming models a streaming interface.
- `addToolInputExamplesMiddleware({ prefix, format, remove })`: serializes a tool's `inputExamples` into its description text for providers that do not natively support `inputExamples`. `prefix` defaults to `'Input Examples:'`, `format` defaults to `JSON.stringify(example.input)`, and `remove` (default `true`) drops `inputExamples` from the tool afterwards.

Steps:
1. Pick the middleware above for the behavior wanted.
2. `wrapLanguageModel({ model, middleware })`.
3. Pass the result as `model` to your calls.

Gotchas:
- Order matters when stacking: the first array entry is the outermost wrapper.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Replaced the cross-skill pointer for addToolInputExamplesMiddleware with its documented options and removed the customProvider and createProviderRegistry gotcha (not on the page).

Method: documentation only; no commands were run.
