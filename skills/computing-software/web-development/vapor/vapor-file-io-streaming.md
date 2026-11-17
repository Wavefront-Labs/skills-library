---
id: computing-software.web-development.vapor.vapor-file-io-streaming
name: vapor-file-io-streaming
category: computing-software
field: web-development
product: vapor
tags: [vapor,fileio,files,streaming,swift,nio,filemiddleware]
level: practitioner
status: docs-checked
description: "Read, stream, collect and write files in Vapor route handlers with req.fileio, and drop to NIO NonBlockingFileIO when needed."
sources:
  - https://docs.vapor.codes/advanced/files/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: read and write files asynchronously from a route handler using `req.fileio` (built on NIO's `NonBlockingFileIO`).

**Read in chunks.** `readFile(at:)` delivers `ByteBuffer` chunks. Relative paths resolve against the process's current working directory.

```swift
let file = try await req.fileio.readFile(at: "/path/to/file")
for try await chunk in file {
    print(chunk) // ByteBuffer
}
```

The future-based form takes a callback: `req.fileio.readFile(at: "/path/to/file") { chunk in ... }` and returns an `EventLoopFuture<Void>` that signals completion or error. With async/await, the read is complete once the loop ends, and errors are thrown.

**Stream as a response.** `req.fileio.streamFile(at: "/path/to/file")` turns a file into a `Response` and sets headers such as `ETag` and `Content-Type` automatically. Return it directly from the handler.

**Collect into memory.** `req.fileio.collectFile(at: "/path/to/file")` reads the whole file into one buffer. Warning from the docs: the entire file must fit in memory, so use chunked or streaming reads to limit memory.

**Write.**

```swift
req.fileio.writeFile(ByteBuffer(string: "Hello, world"), at: "/path/to/file")
```

The returned future signals completion or error.

**Serving the Public folder** automatically is FileMiddleware's job (see the Vapor middleware docs).

**Advanced.** For cases the Vapor API doesn't cover, use NIO's type directly:

```swift
let fileHandle = try await req.application.fileio.openFile(
    path: "/path/to/file",
    eventLoop: req.eventLoop)
```

On the main thread the docs use `app.fileio.openFile(path:eventLoop:)` with `app.eventLoopGroup.next()`, followed by `.get()`.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) advanced/files, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
