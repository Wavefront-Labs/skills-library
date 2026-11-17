---
id: computing-software.web-development.vapor.vapor-eventloop-blocking-work
name: vapor-eventloop-blocking-work
category: computing-software
field: web-development
product: vapor
tags: [vapor,eventloop,eventloopfuture,blocking,threadpool,hop,bcrypt,swift-nio]
level: sme
status: docs-checked
description: "Keep Vapor event loops responsive: stay on req.eventLoop, hop between loops, and move blocking IO or heavy CPU work such as Bcrypt onto the thread pool."
sources:
  - https://docs.vapor.codes/basics/async/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid stalling the event loop that serves many clients.

## Model
Boot usually creates one event loop per CPU core, each with one thread. A connecting client is assigned to one loop for all its communication; the loop tracks state for every client assigned to it. Get the current loop in a route via `req.eventLoop`, outside via `app.eventLoopGroup.next()`.

Warning from the docs: Vapor expects route closures to stay on `req.eventLoop`. If you hop threads, ensure `Request` access and the final response future happen on the request's loop.

Move a future to another loop: `futureString.hop(to: otherEventLoop)`.

## Blocking
Blocking the loop (e.g. `sleep(5)`) delays every other client on that loop, possibly hundreds or thousands. Run blocking work in the background and notify the loop through a promise/future:
```swift
app.get("hello") { req -> EventLoopFuture<String> in
    return req.application.threadPool.runIfActive(eventLoop: req.eventLoop) {
        sleep(5)   // background thread, loops unaffected
        return "Hello world!"
    }
}
```
If unsure a call blocks, research it or ask.

### I/O bound
Waiting on network or disk. Never make blocking I/O calls directly on an event loop. Vapor packages use non-blocking NIO IO, but many Swift packages and C libraries block; a synchronous disk/network function (no callbacks or futures) probably does.

### CPU bound
Most request time is waiting on DB/network, which is fine. Long CPU work on a loop delays faster routes; find it and move it to background threads. It is a gray area, your call where to draw the line. A common example is Bcrypt hashing at signup/login: deliberately slow, so offloading it lets the CPU interleave event-loop work and raises concurrency.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) basics/async, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
