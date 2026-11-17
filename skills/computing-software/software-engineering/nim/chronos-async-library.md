---
id: computing-software.software-engineering.nim.chronos-async-library
name: chronos-async-library
category: computing-software
field: software-engineering
product: nim
tags: [chronos-async-library, async-programming, chronos, async, cancellation, transports, nimbus, nim-chronos, nim]
level: sme
status: docs-checked
description: "Know what Chronos offers (cancellation, raises tracking, socket and HTTP I/O) and how to adopt it via nimble."
sources:
  - https://github.com/status-im/nim-chronos
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chronos: the alternative async runtime

Goal: decide whether to use Chronos.

- Chronos is an async/await framework for Nim from the status-im project. Its README lists: asynchronous socket and process I/O, an HTTP server with SSL/TLS support out of the box (no OpenSSL needed), synchronization primitives (queues, events, locks), cancellation, an efficient multi-platform dispatch pipeline and `raises` tracking for error handling.
- Install with `nimble install chronos`, or add `requires "chronos"` to the `.nimble` file.
- Use pattern from the README: `import chronos/apps/http/httpclient`, an `{.async.}` proc returning `Future[string]`, `HttpSessionRef.new()`, `await httpSession.fetch(parseUri(uri))`, `finally: await httpSession.closeWait()` and `waitFor` at the top level.
- The README marks stability as experimental and lists projects built on it: libp2p, presto, Scorper, websock.
- Documentation is the user guide at status-im.github.io/nim-chronos; check it for the current `raises` annotation syntax before use.
- The README's TODO list includes multithreaded Stream/Datagram servers, so do not assume them.

Gotchas:
- Library code is usually written against one async runtime; choose per ecosystem rather than mixing futures from different runtimes.
- With `raises` tracking, errors must be accounted for in the annotation.

Verify: the README's `retrievePage` example fetches a page and closes the session.

## Checked

2026-11-08. Read in full: the nim-chronos README. Removed: `cancelAndWait`, `Duration`/`Moment`, the `sleepAsync(1.seconds)` example and stream/datagram transport claims, the asyncdispatch comparison, the nim-libp2p/Nimbus attributions and the cancellation-handling gotcha (none in the README); manual, tutorial and lib.html dropped from sources.
Method: documentation only; no commands were run.
