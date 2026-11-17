---
id: computing-software.software-engineering.ktor.ktor-websockets
name: ktor-websockets
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, websockets, kotlin, real-time, sharedflow, server]
level: practitioner
status: docs-checked
description: "Install and configure the Ktor server WebSockets plugin, write webSocket routes, handle frames and close events, and broadcast to many sessions with SharedFlow."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-websockets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor server WebSockets

The WebSockets plugin gives a full-duplex session between browser/client and server over one TCP connection. Dependency: `io.ktor:ktor-server-websockets` (package `io.ktor.server.websocket`).

## Install and configure

Install the plugin, optionally passing `WebSocketOptions` in the `install` block:

- `pingPeriod`: duration between pings.
- `timeout`: timeout after which the connection is closed.
- `maxFrameSize`: maximum Frame that can be received or sent.
- `masking`: whether masking is enabled.
- `contentConverter`: converter for serialization/deserialization.

Extensions such as Deflate or a custom extension can be added too.

## Define an endpoint

```kotlin
routing {
    webSocket("/echo") {
        // Handle a WebSocket session
    }
}
```

With the default configuration this accepts `ws://localhost:8080/echo`. The block receiver is `DefaultWebSocketServerSession`:

- `send` sends text to the client.
- `incoming` / `outgoing` are the frame channels (`Frame`).
- `close` sends a close frame with a reason.
- `call` gives client info such as the IP address.

Check frame types: `Frame.Text` (`readText()`), `Frame.Binary` (`readBytes()`).

Gotcha: `incoming` does NOT contain control frames (ping/pong/close). To handle control frames and reassemble fragmented frames, use `webSocketRaw` instead.

## Map WebSocket events to Ktor

- `onConnect`: the start of the block.
- `onMessage`: after a successful read (`incoming.receive()`) or each step of `for (frame in incoming)`.
- `onClose`: `incoming` is closed, which ends the iteration or throws `ClosedReceiveChannelException` on receive.
- `onError`: any other exception.

`closeReason` is set in both close and error cases:

```kotlin
webSocket("/echo") {
    try {
        for (frame in incoming) {
            val text = (frame as Frame.Text).readText()
            outgoing.send(Frame.Text(text))
        }
    } catch (e: ClosedReceiveChannelException) {
        println("onClose ${closeReason.await()}")
    } catch (e: Throwable) {
        println("onError ${closeReason.await()}")
    }
}
```

## Many sessions

Use a Kotlin `SharedFlow` to broadcast: define one shared flow, and in each route emit incoming messages into it (processed in a `runCatching` block) while collecting from it to send to that client. This avoids manually tracking connections and scales to many concurrent sessions.

For one-way server-to-client updates, the page suggests Server-Sent Events instead.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-websockets.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
