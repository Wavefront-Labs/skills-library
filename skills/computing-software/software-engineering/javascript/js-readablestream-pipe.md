---
id: computing-software.software-engineering.javascript.js-readablestream-pipe
name: js-readablestream-pipe
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, readablestream-pipeto, js-web-streams]
level: advanced
status: docs-checked
description: "Create a ReadableStream with start, pull and cancel, and pipe it with pipeTo options such as signal and preventAbort."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream", "https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/ReadableStream", "https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/pipeTo", "https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/tee", "https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ReadableStream pipeTo and backpressure

- `new ReadableStream({ start(controller) {}, pull(controller) { controller.enqueue(chunk); }, cancel(reason) {} }, queuingStrategy)`. `pull` is called repeatedly until the internal queue is full; `cancel(reason)` runs when the consumer cancels, so release the source there. A `queuingStrategy.highWaterMark` sets how much the queue holds before backpressure applies (default: count strategy, high water mark 1).
- `await readable.pipeTo(writable, options)` returns a promise that fulfils when piping completes and rejects on error. Options include `signal` (an `AbortSignal`), `preventClose`, `preventAbort` and `preventCancel`: `preventAbort: true` stops source errors aborting the destination, `preventClose: true` stops source closing from closing it. It throws if either stream is locked.
- `tee()` returns an array of two branches; cancel both to cancel the source, and the stream stays locked while teed.
- Async iteration over a stream, `for await (const chunk of stream)`, is shown on MDN for `response.body`; a `TypeError` there means the browser lacks it.
- A reader locks the stream until released, and `ReadableStream.locked` reports it.

Self-check: pipe into a slow `WritableStream` and log calls to `pull`; they pace themselves to the queue.

## Checked

2026-11-03. Confirmed on MDN: ReadableStream and its constructor (`start`, `pull`, `cancel`, `queuingStrategy`), pipeTo (return promise, `signal`, `preventAbort`, `preventClose`, locked error), tee, getReader (lock), Using readable streams (async iteration, `pull` semantics). Removed: Node `Readable.toWeb/fromWeb`, `reader.releaseLock()` as an instruction (the page states only that the lock lasts until the reader is released), the "buffers if one branch lags" claim, and the Safari async-iteration remark.
Method: documentation only; no commands were run.
