---
id: computing-software.software-engineering.typescript.node-streams-and-pipeline
name: node-streams-and-pipeline
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, nodejs, node-runtime, node-streams, stream-pipeline, backpressure, web-streams, async-iterators]
level: practitioner
status: verified
description: "Process large data in Node with streams: readable/writable/transform, backpressure, stream.pipeline error handling, async iteration and Web Streams interop."
sources:
  - https://nodejs.org/api/stream.html
  - https://nodejs.org/en/learn/modules/backpressuring-in-streams
  - https://nodejs.org/api/stream.html#streampipelinesource-transforms-destination-options
  - https://nodejs.org/api/webstreams.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node streams and stream.pipeline

**Goal:** process files and network payloads larger than memory, with backpressure and errors handled so nothing leaks.

## 1. Always use pipeline
```ts
import { pipeline } from "node:stream/promises";
import { createReadStream, createWriteStream } from "node:fs";
import { createGzip } from "node:zlib";

await pipeline(
  createReadStream("access.log"),
  createGzip(),
  createWriteStream("access.log.gz"),
);
```
`pipeline` (every snippet in this skill ran on Node 24) propagates errors from any stage, destroys all streams on failure, and respects backpressure. `a.pipe(b)` does **not** forward errors or close the source on destination failure: file descriptors leak and the process may crash on an unhandled `error` event.

## 2. Transforms with async generators
```ts
import { createInterface } from "node:readline";
await pipeline(
  createReadStream("events.jsonl"),
  async function* (source) {
    let buf = "";
    for await (const chunk of source) {
      buf += chunk;
      const lines = buf.split("\n"); buf = lines.pop()!;
      for (const l of lines) if (l) yield JSON.stringify(transform(JSON.parse(l))) + "\n";
    }
    if (buf) yield JSON.stringify(transform(JSON.parse(buf))) + "\n";
  },
  createWriteStream("out.jsonl"),
);
```
For line splitting, `readline.createInterface({ input, crlfDelay: Infinity })` is an async iterable of lines.

## 3. Backpressure when writing manually
```ts
import { once } from "node:events";
for (const row of rows) {
  if (!out.write(serialize(row))) await once(out, "drain");   // write() false = buffer above highWaterMark
}
out.end();
await once(out, "finish");
```
Ignoring `write()`'s return value buffers unboundedly in memory.

## 4. Object mode and Transform class
```ts
import { Transform } from "node:stream";
const toUpper = new Transform({
  objectMode: true,
  transform(rec, _enc, cb) { cb(null, { ...rec, name: rec.name.toUpperCase() }); },
});
```
`highWaterMark` counts bytes or objects (16 in object mode). The byte default is 64 KiB on non-Windows platforms and 16 KiB on Windows (Node 24 `stream.getDefaultHighWaterMark` docs; measured 16384 on Windows, while `fs.createReadStream` read 65536).

## 5. Web Streams interop
`fetch()` bodies are Web `ReadableStream`s:
```ts
import { Readable } from "node:stream";
const res = await fetch(url);
await pipeline(Readable.fromWeb(res.body!), createWriteStream("file.bin"));
```
`Readable.toWeb()`/`Writable.toWeb()` go the other way.

## Gotchas
- Mixing `data` event listeners with `for await` or `pipe` puts streams in flowing mode unexpectedly; choose one consumption style.
- Multi-byte characters split across chunks: use `setEncoding("utf8")` or a `StringDecoder`, not `chunk.toString()` per chunk.
- HTTP responses: a client disconnect destroys the response; `pipeline` surfaces it as `ERR_STREAM_PREMATURE_CLOSE` (reproduced with a destination that destroys itself), which is often expected and can be logged at debug.
- Abort a pipeline with `pipeline(..., { signal })` and an `AbortController` (tested: rejects with `AbortError`, code `ABORT_ERR`).

## Verify
- Process a file larger than available heap (`node --max-old-space-size=128`) without OOM, and kill the destination mid-way to confirm the source file descriptor closes (no `EMFILE` over repeated runs).
