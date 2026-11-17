---
id: computing-software.web-development.frontend-development.streaming-fetch-responses
name: streaming-fetch-responses
category: computing-software
field: web-development
product: frontend-development
tags: [fetch-api, browser-networking, readablestream, streaming-fetch, textdecoderstream, ndjson, streaming-llm-responses, response-body]
level: practitioner
status: docs-checked
description: "Consuming streamed fetch responses with ReadableStream and TextDecoderStream: incremental rendering, NDJSON parsing, progress and cancellation."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams
  - https://developer.mozilla.org/en-US/docs/Web/API/TextDecoderStream
  - https://developer.chrome.com/docs/capabilities/web-apis/fetch-streaming-requests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming fetch responses

**Goal:** render data as it arrives (logs, search results, LLM tokens, large exports) instead of waiting for the whole body.

## 1. Read text chunks
```js
const res = await fetch('/api/stream', { signal });
const reader = res.body.pipeThrough(new TextDecoderStream()).getReader();
while (true) {
  const { value, done } = await reader.read();
  if (done) break;
  output.append(value);          // value is a string chunk, NOT a line or message
}
```
Chunk boundaries are arbitrary: a JSON object can be split across chunks. `TextDecoderStream` converts a stream of bytes in an encoding such as UTF-8 into a stream of strings; you handle message framing.

## 2. NDJSON (newline-delimited JSON) framing
```js
async function* ndjson(res) {
  let buf = '';
  for await (const chunk of res.body.pipeThrough(new TextDecoderStream())) {   // async iteration of ReadableStream: Chrome 124, Firefox 110, Safari 27 (MDN BCD); use getReader() for older browsers
    buf += chunk;
    let i;
    while ((i = buf.indexOf('\n')) >= 0) {
      const line = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
      if (line) yield JSON.parse(line);
    }
  }
  if (buf.trim()) yield JSON.parse(buf);
}
for await (const row of ndjson(res)) addRow(row);
```

## 3. Download progress
```js
const total = Number(res.headers.get('content-length')) || 0;   // may be absent (for example with chunked responses)
let loaded = 0;
const counted = res.body.pipeThrough(new TransformStream({ transform(c, ctl) { loaded += c.byteLength; progress(loaded, total); ctl.enqueue(c); } }));
const blob = await new Response(counted).blob();
```
With a `Content-Encoding`, `content-length` describes the encoded body while the stream yields decoded bytes, so progress can overshoot; show indeterminate progress if unsure.

## 4. Server side must actually stream
Proxies and frameworks may buffer responses: disable buffering (MDN's server-sent-events example sets `X-Accel-Buffering: no` for nginx), flush after each write, and avoid compression middleware that buffers. Check with a client that does not buffer.

## 5. Cancel
Aborting the fetch with an `AbortController` stops the request (MDN's `for await` example does this to stop iterating), and `reader.cancel()` cancels the stream.

## Verify
- [ ] Items appear incrementally in the UI (not all at the end) on a throttled connection.
- [ ] Messages split across chunks parse correctly (test with a server that writes 1 byte at a time).
- [ ] Navigating away cancels the request (Network panel shows canceled).

## Checked

Checked 2026-10-26 against MDN Using readable streams and TextDecoderStream (mdn/content main) and MDN browser-compat-data api/ReadableStream.json: `for await` over `response.body` works because ReadableStream is async iterable (Chrome 124, Firefox 110, Safari 27 per BCD, so the old 'use getReader in Safari' advice was stale), abort via AbortController, and TextDecoderStream semantics. Removed the unconfirmed nginx `proxy_buffering` and `curl -N` advice and the claim that cancelling notifies the server.

Method: documentation only; no commands were run.
