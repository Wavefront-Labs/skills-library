---
id: computing-software.web-development.trpc.http-batch-stream-link
name: http-batch-stream-link
category: computing-software
field: web-development
product: trpc
tags: [trpc, httpbatchstreamlink, streaming, jsonl, async-generator]
level: advanced
status: docs-checked
description: "Use httpBatchStreamLink to stream batched responses as they finish and to consume async generators, with its limits for headers, Lambda, Workers and React Native."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/httpBatchStreamLink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`httpBatchStreamLink` batches like `httpBatchLink` but streams each response as soon as it is ready instead of waiting for the whole batch. It is required for procedures that return async generators or promises nested in output; a regular `httpLink` or `httpBatchLink` gets the server response `Cannot use stream-like response in non-streaming request - use httpBatchStreamLink`.

```ts
createTRPCClient<AppRouter>({
  links: [httpBatchStreamLink({ url: 'http://localhost:3000' })],
});

const iterable = await trpc.examples.iterable.query();
for await (const value of iterable) console.log(value);
```

Differences from `httpBatchLink`:
- Requests carry `trpc-accept: application/jsonl`. The `streamHeader: 'accept'` option uses the standard `Accept` header instead, which is CORS-safelisted and can avoid preflight on cross-origin streaming queries.
- Responses use `transfer-encoding: chunked` and default to `content-type: application/json`. Change it with `initTRPC.create({ jsonl: { contentType: 'application/jsonl' } })`; `jsonl.pingMs` configures pings.
- `responseMeta` no longer receives `data`, because headers are sent before data exists.

You cannot set response headers or cookies from a procedure once the stream has begun; use `httpBatchLink` when you need that.

Compatibility: non-browser runtimes need a streaming `fetch` (response body as `ReadableStream`); undici, node-fetch and native fetch qualify. React Native lacks `TextDecoder` and `TextDecoderStream`, so polyfill them and supply a streaming fetch (for example `react-native-fetch-api` with `reactNative: { textStreaming: true }`, or `fetch` from `expo/fetch`). AWS Lambda only streams when infrastructure is set up for response streaming, otherwise it acts like `httpBatchLink`. Cloudflare Workers needs the `streams_enable_constructors` flag.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): client/links/httpBatchStreamLink.md, client/links.md (Common mistakes). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.
