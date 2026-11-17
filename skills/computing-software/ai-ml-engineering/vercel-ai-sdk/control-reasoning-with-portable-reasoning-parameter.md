---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.control-reasoning-with-portable-reasoning-parameter
name: control-reasoning-with-portable-reasoning-parameter
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [reasoning, settings, provider-options, migration, streaming]
level: practitioner
status: docs-checked
description: "Use the top-level reasoning parameter across providers, read reasoning output, understand value rounding and precedence, and migrate from providerOptions."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/reasoning
  - https://ai-sdk.dev/docs/ai-sdk-core/settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: set reasoning effort once with `reasoning` on `generateText` / `streamText` and let each provider translate it.

## Use it
```ts
const { text, reasoning, reasoningText } = await generateText({
  model: 'anthropic/claude-sonnet-5.5',
  reasoning: 'medium',
  prompt: 'How many people will live in the world in 2040?',
});
```
Values: `'provider-default'` (when omitted), `'none'`, `'minimal'`, `'low'`, `'medium'`, `'high'`, `'xhigh'`, `'max'`. Streaming reads parts from `result.stream`:
```ts
for await (const part of result.stream) {
  if (part.type === 'reasoning') process.stdout.write(part.textDelta);
  else if (part.type === 'text-delta') process.stdout.write(part.textDelta);
}
```

## Mapping rules
- Order is none < minimal < low < medium < high < xhigh < max. If a model lacks the requested level the provider rounds down (xhigh becomes high); if nothing lower exists it uses the next higher.
- Rounding never turns reasoning off. `'none'` on a model that cannot disable reasoning maps to its lowest level.
- A `compatibility` warning is emitted whenever the value sent differs from the one requested; models that do not support reasoning configuration emit `unsupported` and ignore it.
- Rounding only happens for model IDs the provider recognizes. Unrecognized IDs (fine-tuned, custom), OpenAI-compatible and Open Responses endpoints get the value directly and the API decides.
- Token-budget providers map the value to a percentage of the model's max output tokens (`'max'` is 95% by default), within provider limits.

## Precedence and migration
Provider-specific settings win over fields derived from `reasoning`; partial provider configs still get missing fields filled from it.
```ts
// before: providerOptions: { anthropic: { thinking: { type: 'adaptive' }, effort: 'high' } }
reasoning: 'high'
// keep summaries or display settings alongside it
reasoning: 'high', providerOptions: { openai: { reasoningSummary: 'auto' } }
reasoning: 'high', providerOptions: { google: { thinkingConfig: { includeThoughts: true } } }
```
`providerOptions.openai.reasoningEffort: 'high'` overrides `reasoning: 'low'`. If you need an exact token budget (for example 12000), keep `providerOptions`.

## Gotchas
- `'max'` can raise token use, latency, cost and the chance of hitting request or output limits.
- The docs keep provider-specific display settings alongside `reasoning`, for example Google `thinkingConfig.includeThoughts`.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the invented Verify step (result.warnings) and softened the Google includeThoughts gotcha.

Method: documentation only; no commands were run.
