---
id: computing-software.software-engineering.java.websocket-client-in-java-net-http
name: websocket-client-in-java-net-http
category: computing-software
field: software-engineering
product: java
tags: [java, java-net-http, websocket, backpressure, ping-pong, reconnect, client]
level: practitioner
status: docs-checked
description: "Open a WebSocket client with java.net.http (Java 11+): Listener callbacks, request(n) backpressure, partial messages, ping/pong, the close handshake and reconnects."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.net.http/java/net/http/WebSocket.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.net.http/java/net/http/WebSocket.Builder.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.net.http/java/net/http/WebSocket.Listener.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebSocket client (java.net.http)

## Connect
```java
WebSocket ws = HttpClient.newHttpClient().newWebSocketBuilder()
    .connectTimeout(Duration.ofSeconds(5))
    .header("Authorization", "Bearer " + token)
    .buildAsync(URI.create("wss://stream.example.com/feed"), new WebSocket.Listener() {
        private final StringBuilder buf = new StringBuilder();
        @Override public void onOpen(WebSocket w) { w.request(1); }
        @Override public CompletionStage<?> onText(WebSocket w, CharSequence data, boolean last) {
            buf.append(data);
            if (last) { handle(buf.toString()); buf.setLength(0); }
            w.request(1);                      // ask for the next receive call
            return null;
        }
        @Override public CompletionStage<?> onClose(WebSocket w, int code, String reason) {
            scheduleReconnect(); return null;
        }
        @Override public void onError(WebSocket w, Throwable t) { log.error("ws", t); }
    }).join();
```
`handle`, `scheduleReconnect` and `log` are your own code.

## Key behaviours
1. **Backpressure:** `request(n)` raises a counter of receive-method calls (`onText`, `onBinary`, `onPing`, `onPong`, `onClose`); while it is zero the WebSocket invokes none of them, and a new WebSocket starts at zero. Forgetting `request` after `onOpen` or after each message stalls the stream. `n` counts invocations, not messages, and `n <= 0` throws `IllegalArgumentException`.
2. Text and binary messages can arrive in fragments (`last == false`); accumulate until `last` is true.
3. The `CompletionStage` returned from a receive method signals when the data (`CharSequence`/`ByteBuffer`) may be reclaimed; it does not gate further invocations, which are governed by `request`. Return `null` for "reclaimable now".
4. Sends are asynchronous. `sendText(CharSequence, boolean last)` returns a `CompletableFuture<WebSocket>`; starting a text/binary send while one is pending completes the future exceptionally with `IllegalStateException`. Chain with `thenCompose` or queue messages. Do not modify the data until the future completes.
5. Pings and Close messages from the server are answered automatically. Send your own ping with `sendPing(ByteBuffer)` (at most 125 bytes; only one ping/pong send may be pending).
6. Close: `ws.sendClose(WebSocket.NORMAL_CLOSURE, "bye")` closes the output side only (reason at most 123 UTF-8 bytes); the input stays open until a Close message arrives, `abort()` is called or an error occurs. `abort()` closes both sides abruptly and fails pending sends with `IOException`.

## Gotchas
- There is no automatic reconnect; implement exponential backoff with jitter and resubscribe state.
- If a listener method throws, or its returned stage completes exceptionally, the WebSocket invokes `onError` with that exception. After `onError` or `onClose` no further listener methods are invoked.
- `connectTimeout` on the builder bounds connection establishment only.

## Verify
Run against a local echo server; send 100 messages and assert all are echoed in order, then simulate a server close and assert the reconnect path.

## Checked
2026-11-03. Confirmed against the Java SE 21 API pages for WebSocket, WebSocket.Builder and WebSocket.Listener: builder methods (connectTimeout, header, buildAsync), request(n) counter semantics, send-method behaviour and IllegalStateException on pending sends, automatic ping/close replies, sendPing limit, sendClose and abort semantics, onError rules, NORMAL_CLOSURE.
Fixed: a second send does not throw, its future completes exceptionally; the returned CompletionStage does not pause delivery. Removed: the HTTP/1.1 upgrade claim and the reference to a Spring skill not in these sources.
Method: documentation only; no commands were run.
