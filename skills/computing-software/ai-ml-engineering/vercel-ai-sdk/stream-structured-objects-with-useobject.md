---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.stream-structured-objects-with-useobject
name: stream-structured-objects-with-useobject
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [object-generation, useobject, output-object, output-choice, zod, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Stream a partial JSON object into React with useObject and a streamText route using Output.object or Output.choice with a shared Zod schema."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/object-generation
  - https://ai-sdk.dev/docs/reference/ai-sdk-ui/use-object
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stream structured objects with useObject

Goal: render a JSON object progressively while the model generates it, validated against a schema.

## Shared schema (imported by client and server)

```ts
export const notificationSchema = z.object({
  notifications: z.array(z.object({
    name: z.string().describe('Name of a fictional person.'),
    message: z.string().describe('Message. Do not use emojis or links.'),
  })),
});
```

## Server: text stream, not UI message stream

```ts
import { createTextStreamResponse, Output, streamText, toTextStream } from 'ai';
const result = streamText({ model, output: Output.object({ schema: notificationSchema }), prompt: `Generate 3 notifications ... ${context}` });
return createTextStreamResponse({ stream: toTextStream({ stream: result.stream }) });
```

`context` is the JSON body that `submit(input)` posts.

## Client

```tsx
import { useObject } from '@ai-sdk/react';
const { object, submit, isLoading, error, stop, clear } = useObject({ api: '/api/notifications', schema: notificationSchema });
// <button onClick={() => submit('Messages during finals week.')}>
// {object?.notifications?.map((n, i) => <p key={i}>{n?.name}</p>)}
```

`object` is a `DeepPartial`, so guard every level with `?.`. `schema` may be Zod or `jsonSchema(...)`. Svelte exports `StructuredObject`, Vue `useObject`; Angular has an equivalent `StructuredObject` service.

## Classification (enum mode)

Client schema must be an object keyed `enum`: `schema: z.object({ enum: z.enum(['true', 'false']) })`, read `object.enum`. Server uses `output: Output.choice({ options: ['true', 'false'] })` with the same `createTextStreamResponse` / `toTextStream` pair.

## Options and callbacks

- `useObject` options: `api`, `schema`, `id` (shared state), `initialValue`, `fetch`, `headers`, `credentials`, `onError`, `onFinish`.
- `onFinish({ object, error })`: `object` is undefined when final validation fails, in which case `error` is e.g. a `TypeValidationError`. `onError` covers fetch failures.
- Use `isLoading` to disable the submit button or show Stop (`stop()`), and show a generic message on `error`.

## Gotchas

- The docs routes return a text stream (`createTextStreamResponse` with `toTextStream`), and `useObject` consumes text streams.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Replaced the "unlike useChat routes" gotcha with what the docs routes do.

Method: documentation only; no commands were run.
