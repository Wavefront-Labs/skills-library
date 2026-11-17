---
id: computing-software.software-engineering.javascript.js-transformstream-compression
name: js-transformstream-compression
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, transformstream, js-web-streams]
level: advanced
status: docs-checked
description: "Compose stream transforms: CompressionStream and DecompressionStream formats, TextDecoderStream and custom TransformStream transform and flush."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/TransformStream", "https://developer.mozilla.org/en-US/docs/Web/API/CompressionStream", "https://developer.mozilla.org/en-US/docs/Web/API/CompressionStream/CompressionStream", "https://developer.mozilla.org/en-US/docs/Web/API/DecompressionStream", "https://developer.mozilla.org/en-US/docs/Web/API/TextDecoderStream"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TransformStream, CompressionStream and text decoding

- A `TransformStream` is passed to `ReadableStream.pipeThrough()` to convert data from one form to another (decode, decompress, XML to JSON). If no transformation is supplied, data passes through unmodified.
- Custom transform: `new TransformStream({ transform(chunk, controller) { controller.enqueue(f(chunk)); }, flush(controller) {} })`.
- `new CompressionStream(format)` accepts `"gzip"`, `"deflate"` or `"deflate-raw"`; `DecompressionStream` is the inverse. Example: `blob.stream().pipeThrough(new DecompressionStream("gzip"))`.
- `TextDecoderStream` is the streaming `TextDecoder`: it turns a stream of bytes in an encoding such as UTF-8 into a stream of strings and can be used in `pipeThrough()`.
- `pipeThrough(transform, options)` accepts the same `preventClose`, `preventAbort` and `preventCancel` options as `pipeTo()`.

Self-check: compress then decompress a blob and compare the bytes.

## Checked

2026-11-03. Confirmed on MDN: TransformStream (purpose, optional transform, `transform`/`flush` in the example), CompressionStream and its constructor (gzip, deflate, deflate-raw), DecompressionStream (gzip example from a Blob), TextDecoderStream, ReadableStream.pipeThrough options. Removed: the claim that chunk boundaries can split UTF-8 characters or lines and need a remainder buffer, `fetch` streaming uploads with `duplex: "half"` (Chromium, HTTP/2), and the statement that errors in any stage abort the whole pipeline.
Method: documentation only; no commands were run.
