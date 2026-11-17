---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.fix-ai-sdk-streaming-not-working-when-deployed-or-proxied
name: fix-ai-sdk-streaming-not-working-when-deployed-or-proxied
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [troubleshooting, streaming, proxy, headers, maxduration, vercel, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Diagnose AI SDK responses that arrive all at once behind a host or proxy, or get cut off by Vercel timeouts, using stream headers and maxDuration."
sources:
  - https://ai-sdk.dev/docs/troubleshooting/streaming-not-working-when-deployed
  - https://ai-sdk.dev/docs/troubleshooting/streaming-not-working-when-proxied
  - https://ai-sdk.dev/docs/troubleshooting/timeout-on-vercel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fix streaming that breaks when deployed, proxied or timed out

Goal: get token-by-token streaming and complete responses outside local development.

## Symptom A: works locally, only the full response arrives after a delay (deployed)

Causes depend on the environment. Try adding chunked-transfer and keep-alive headers to the stream response:

```ts
return createUIMessageStreamResponse({
  stream: toUIMessageStream({ stream: result.stream }),
  headers: { 'Transfer-Encoding': 'chunked', Connection: 'keep-alive' },
});
```

## Symptom B: no streaming in local dev or behind a proxy

The docs attribute this to proxy middleware that compresses the response, which defeats streaming. Add `'Content-Encoding': 'none'` to the same `headers` option. The fix only affects the streaming API route.

## Symptom C: long responses cut off on Vercel

Logs show timeouts, or the client throws `Uncaught (in promise) Error: Connection closed`.

- With Vercel Fluid Compute the default function duration is 5 minutes (300 seconds) on all plans.
- To extend it in Next.js App Router, export from the route file (or the page that calls a Server Action): `export const maxDuration = 600;`
- For other frameworks set it in `vercel.json` under `functions`, for example `"api/chat/route.ts": { "maxDuration": 600 }`.
- Limits by plan: Hobby up to 300 seconds, Pro and Enterprise up to 800 seconds. Values above 300 need Pro or Enterprise.

## Checked

Date: 2026-11-07. Read the 3 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the Gotchas section (10 second Hobby default and a duplicate note, neither on the cited pages).

Method: documentation only; no commands were run.
