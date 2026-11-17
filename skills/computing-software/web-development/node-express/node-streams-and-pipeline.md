---
id: computing-software.web-development.node-express.node-streams-and-pipeline
name: node-streams-and-pipeline
category: computing-software
field: web-development
product: node-express
tags: [node, node-streams, stream-pipeline, backpressure, transform-streams, async-iterators, web-streams, web-development]
level: practitioner
status: verified
description: "Using Node.js streams safely: stream/promises pipeline, backpressure, async-generator transforms, error and abort handling, and web stream interop."
sources:
  - https://nodejs.org/api/stream.html#streampipelinesource-transforms-destination-options
  - https://nodejs.org/en/learn/modules/backpressuring-in-streams
  - https://nodejs.org/api/stream.html#streams-promises-api
  - https://nodejs.org/api/webstreams.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streams and pipeline with backpressure

**Goal:** process large files and responses in constant memory, with every error and abort cleaning up all stages.

## 1. Use pipeline, not pipe
```js
import { pipeline } from "node:stream/promises";
import { createReadStream, createWriteStream } from "node:fs";
import { createGzip } from "node:zlib";

await pipeline(createReadStream("big.log"), createGzip(), createWriteStream("big.log.gz"));
```
`a.pipe(b)` doesn't forward errors or destroy other streams on failure (leaked file descriptors, hanging responses). `pipeline` destroys every stage on error and rejects once.

## 2. Transforms as async generators
```js
import { createInterface } from "node:readline";
await pipeline(
  createReadStream("users.csv"),
  async function* (source) {
    let buf = "";
    for await (const chunk of source) {
      buf += chunk;
      const lines = buf.split("\n"); buf = lines.pop();
      for (const l of lines) yield JSON.stringify(parse(l)) + "\n";
    }
    if (buf) yield JSON.stringify(parse(buf)) + "\n";
  },
  createWriteStream("users.ndjson"),
);
```
Line-by-line reading: `for await (const line of createInterface({ input: createReadStream(f), crlfDelay: Infinity }))`.

## 3. Backpressure
`writable.write()` returns `false` when the internal buffer exceeds `highWaterMark` (16 KiB bytes / 16 objects by default). Pipeline and `for await` respect it. Manual loops must wait:
```js
import { once } from "node:events";
if (!out.write(chunk)) await once(out, "drain");
```

## 4. HTTP responses
```js
app.get("/export", async (req, res, next) => {
  res.type("text/csv");
  try { await pipeline(db.queryStream(sql), toCsv(), res, { signal: AbortSignal.timeout(60_000) }); }
  catch (err) { if (!res.headersSent) next(err); else res.destroy(err); }
});
```
If the client disconnects, `res` closes and pipeline tears down the DB stream too.

## 5. Object mode and Readable.from
`Readable.from(iterable)` builds a stream from arrays/generators (object mode by default). Don't mix object-mode and byte streams without a serialising transform.

## 6. Web streams interop
`Readable.toWeb(nodeStream)`, `Readable.fromWeb(webStream)`; `fetch` response bodies are web streams: `await pipeline(Readable.fromWeb(res.body), createWriteStream(f))`.

## Verify
- [ ] Memory stays flat processing a file larger than RAM (`process.memoryUsage().rss` logging).
- [ ] Killing the client mid-download closes the source (log in `close` handler / DB cursor closed).
- [ ] An error in the middle stage rejects the pipeline and leaves no open fds (`lsof -p`).

## Checked
- Node 24.22.0 and 20.20.2: `pipeline` with gzip produced a valid file; the async-generator CSV-to-NDJSON transform and `readline` `for await` read 3 lines; an error in the middle stage rejected once and left source, middle and destination `destroyed`, while `a.pipe(b).pipe(c)` left source and destination undestroyed; default `highWaterMark` is 16384 bytes for byte streams and 16 for object-mode writables (`Readable.from` uses 1); `write()` returned `false` for a 20 KB chunk and `drain` followed; `Readable.toWeb`/`fromWeb` and a `fetch` body piped through `Readable.fromWeb`; `pipeline` with `AbortSignal.timeout` rejected with `AbortError` and destroyed the source (note: that timer does not keep the process alive on its own). The Express export route, DB cursor cleanup and fd-leak check were not run.
