---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.define-function-tools-with-tool-helper
name: define-function-tools-with-tool-helper
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [tool-calling, tool-helper, input-schema, strict-mode, input-examples, dynamic-tool]
level: practitioner
status: docs-checked
description: "Define typed tools with tool(): inputSchema, execute options, strict, inputExamples, toModelOutput, input hooks, dynamicTool, and extracting tools into files."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling
  - https://ai-sdk.dev/docs/reference/ai-sdk-core/tool
  - https://ai-sdk.dev/docs/reference/ai-sdk-core/dynamic-tool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: write a tool the model can call, with correct typing and the options that matter.

```ts
import { tool } from 'ai';
import { z } from 'zod';
export const weatherTool = tool({
  description: 'Get the weather in a location',
  inputSchema: z.object({ location: z.string().describe('The location to get the weather for') }),
  strict: true,
  inputExamples: [{ input: { location: 'San Francisco' } }],
  execute: async ({ location }, { toolCallId, messages, abortSignal }) => ({ location, temperature: 72 }),
});
```
`tool()` has no runtime behaviour; it lets TypeScript connect `inputSchema` and `contextSchema` to callback types, so always use it, especially when extracting tools into separate files. The `tools` parameter is an object keyed by tool name.

## Options (reference)
- `description`: string or `({ context, experimental_sandbox }) => string` resolved before each model call.
- `inputSchema` (required for function tools): Zod or `jsonSchema()`. Add `.describe()` on fields.
- `execute`: optional; without it the call is not run automatically (forward to client or queue). May return a value, a Promise, or an `AsyncIterable`.
- `strict`: boolean, off by default; providers that support it only emit calls valid for the schema, but not every schema is supported. Ignored where unsupported.
- `inputExamples`: `Array<{ input }>`; only Anthropic providers use them natively, others ignore them.
- `outputSchema`: type inference. `contextSchema`: types `context` (see runtime-and-tool-context).
- `toModelOutput({ toolCallId, input, output })`: map the result to model content (default is a JSON result). It runs in `convertToModelMessages`, so pass the same tools there and to `streamText`.
- Input hooks: `onInputStart`, `onInputDelta({ inputTextDelta })` (streaming only), `onInputAvailable({ input })`. `onInputStart` always precedes `onInputAvailable`, even in `generateText`.
- `metadata` (JSON object) lands on the resulting call's `toolMetadata`; `providerOptions` pass through; `deferLoading` hides the tool until tool search.
- `execute` options: `toolCallId`, `messages` (history sent to the model, without system prompt or the assistant tool-call response), `abortSignal`, `context`, `experimental_sandbox`.
- `needsApproval` is deprecated (use `toolApproval` on the call); `title` is deprecated (use `providerMetadata`).

## Dynamic tools
`dynamicTool({ description, inputSchema, execute })` types input/output as `unknown`; cast or validate at runtime (use `z.unknown()` or `z.any()` for fully dynamic inputs; a schema is still required). Returns a tool with `type: 'dynamic'`. In results, branch on `toolCall.dynamic` to narrow types; in `useChat` they appear as `dynamic-tool` parts.

## Gotchas
- Pass the same `tools` to `convertToModelMessages` and to `streamText` (or other generation APIs); `toModelOutput` is invoked in `convertToModelMessages`.
- The docs say to define your own AI SDK tools for most production use (full control, type safety, performance); MCP tools suit rapid iteration and user-supplied tools.

## Checked

Date: 2026-11-07. Read the 3 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Corrected "before each step" to before each model call; corrected the deprecation line (title uses providerMetadata); reworded two gotchas to the docs wording.

Method: documentation only; no commands were run.
