---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.stream-tool-progress-and-multimodal-tool-results
name: stream-tool-progress-and-multimodal-tool-results
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [tool-calling, preliminary-results, to-model-output, multimodal-tool-results, tool-call-id]
level: advanced
status: docs-checked
description: "Yield preliminary tool results from generator execute functions, write custom status data by toolCallId, and return screenshots through toModelOutput."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling
  - https://ai-sdk.dev/docs/reference/ai-sdk-core/tool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: show tool progress to users and send non-text tool output back to the model.

## Preliminary results with async generators
`execute` may return an `AsyncIterable`; every value but the last is preliminary, the last is the final result.
```ts
tool({
  description: 'Get the current weather.',
  inputSchema: z.object({ location: z.string() }),
  async *execute({ location }) {
    yield { status: 'loading' as const, text: `Getting weather for ${location}`, weather: undefined };
    const temperature = 72 + Math.floor(Math.random() * 21) - 10;
    yield { status: 'success' as const, text: `The weather in ${location} is ${temperature}F`, temperature };
  },
});
```
A streaming tool holds its `toolCallConcurrency` slot until its final output or error.

## Custom status data with toolCallId
`execute` gets `{ toolCallId }` as the second argument. In a route handler create a UI stream and write data parts keyed by that id, then merge the model stream:
```ts
const stream = createUIMessageStream({
  execute: ({ writer }) => {
    const result = streamText({ /* ..., tools: { myTool: tool({
      execute: async (args, { toolCallId }) => {
        writer.write({ type: 'data-tool-status', id: toolCallId, data: { name: 'myTool', status: 'in-progress' } });
      } }) } */ });
    writer.merge(toUIMessageStream({ stream: result.stream }));
  },
});
return createUIMessageStreamResponse({ stream });
```

## Multi-modal tool results (experimental)
Supported by Anthropic, OpenAI and Google (Gemini 3 models). Convert the raw result with `toModelOutput({ output })`:
```ts
toModelOutput({ output }) {
  return { type: 'content', value: typeof output === 'string'
    ? [{ type: 'text', text: output }]
    : [{ type: 'file', mediaType: 'image/png', data: { type: 'data', data: output.data } }] };
}
```
Google specifics: use base64 inline-data file parts (`data: { type: 'data', data }`) or base64 `data:` URLs in URL-style parts; remote HTTP(S) URLs in tool-result URL parts are not supported. Vertex also supports `gs://` references for Gemini 3 and later and downloads HTTP(S) URLs into inline data.

## Gotchas
- The default (no `toModelOutput`) sends results as JSON.
- `toModelOutput` runs inside `convertToModelMessages`; pass the same tools there.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
