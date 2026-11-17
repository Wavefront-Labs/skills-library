---
id: computing-software.software-engineering.javascript.js-web-streams-api
name: js-web-streams-api
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-web-streams, readablestream, transformstream, backpressure, compression-stream]
level: advanced
status: docs-checked
description: "Use ReadableStream, TransformStream and the built-in stream types in browsers: piping, readers and locks, tee, queuing strategy and cancellation."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Streams_API", "https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams", "https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/ReadableStream", "https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/getReader", "https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/tee", "https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/pipeThrough", "https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/pipeTo"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web Streams

- `ReadableStream` is a source, `WritableStream` a sink, `TransformStream` a writable/readable pair. Chain `readable.pipeThrough(transform).pipeTo(writable)`; `pipeTo()` returns a promise that fulfils when piping completes and rejects on error.
- Consume with `const reader = stream.getReader(); for (;;) { const { done, value } = await reader.read(); if (done) break; }`, or `for await (const chunk of response.body)` where async iteration is supported (a `TypeError` can mean the browser lacks it).
- `getReader()` locks the stream until the reader is released; a second reader on a locked stream throws. `ReadableStream.locked` reports the state. `tee()` returns two branches; you must cancel both branches to cancel the stream, and the stream stays locked while teed.
- Backpressure: the constructor's `queuingStrategy` has a `highWaterMark`, the total chunk size the internal queue may hold before backpressure applies (default is a `CountQueuingStrategy` with a high water mark of 1). `pull(controller)` is called repeatedly until the internal queue is full.
- A source's `cancel(reason)` is called when the consumer cancels; release the underlying resource there.
- Built-ins: `response.body` from `fetch`, `Blob.stream()`, `TextDecoderStream`, `CompressionStream` and `DecompressionStream`.

## Checked

2026-11-03. Confirmed on MDN: Streams API, Using readable streams (reader loop, `done`, `pull` semantics, async iteration of `response.body`), ReadableStream constructor (`queuingStrategy`, `highWaterMark`, default, `cancel`), getReader (locking, errors), tee, pipeThrough, pipeTo, TransformStream, TextDecoderStream, CompressionStream. Removed: `controller.desiredSize`, Node `stream/web` and `Readable.fromWeb/toWeb` bridges, and the Node 18+ claim, none of which appears on a page read; also the ECMAScript and MDN JavaScript root sources.
Method: documentation only; no commands were run.
