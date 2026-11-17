---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.set-agent-call-options
name: set-agent-call-options
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [call-options, calloptionsschema, preparecall, toolloopagent, createagentuistreamresponse]
level: practitioner
status: docs-checked
description: "Pass typed per-request options to an agent with callOptionsSchema and prepareCall to change instructions, model, tools, activeTools or providerOptions."
sources:
  - https://ai-sdk.dev/docs/agents/configuring-call-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: one agent, request-specific behavior, with TypeScript checking the inputs.

Three steps: define `callOptionsSchema`, modify settings in `prepareCall`, pass `options` at call time.

```ts
const supportAgent = new ToolLoopAgent({
  model: 'openai/gpt-6-luna',
  callOptionsSchema: z.object({ userId: z.string(), accountType: z.enum(['free', 'pro', 'enterprise']) }),
  instructions: 'You are a helpful customer support agent.',
  prepareCall: ({ options, ...settings }) => ({
    ...settings,
    instructions: settings.instructions + `\nUser context:\n- Account type: ${options.accountType}\n- User ID: ${options.userId}`,
  }),
});

await supportAgent.generate({ prompt: 'How do I upgrade my account?', options: { userId: 'user_123', accountType: 'free' } });
```

Key rules:
- `options` becomes required and type-checked on `generate()` / `stream()`.
- The object returned by `prepareCall` replaces the call settings, so always spread `...settings` and override only what changes.
- `prepareCall` may be async (for example `await vectorSearch(options.query)` then put documents in `instructions` for RAG).

Settings you can override from options:
- `model` (for example `'openai/gpt-6-luna'` for simple, `'openai/gpt-6-astra'` for complex).
- `tools` (rebuild a tool with request data, such as `openai.tools.webSearch({ searchContextSize: 'low', userLocation: { type: 'approximate', city, region, country: 'US' } })`).
- `providerOptions`, for example `{ openai: { reasoningEffort: options.taskDifficulty } satisfies OpenAILanguageModelResponsesOptions }`.
- `activeTools`, for example `['readDatabase', 'writeDatabase']` for admins and `['readDatabase']` otherwise, alongside `instructions` and `model` in one return.

API route: `createAgentUIStreamResponse({ agent: myAgent, messages, options: { userId, accountType } })`.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the toolsContext and runtimeContext gotcha (not on the page).

Method: documentation only; no commands were run.
