---
id: computing-software.software-engineering.quarkus.quarkus-websockets-next-endpoints
name: quarkus-websockets-next-endpoints
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, websockets-next, websocket, callbacks, mutiny, server-endpoint]
level: practitioner
status: docs-checked
description: "Build WebSockets Next server endpoints in Quarkus: @WebSocket paths, callback methods, return types, blocking rules, Multi streams, connections, codecs, errors."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/websockets-next-reference.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebSockets Next server endpoints

Dependency: `io.quarkus:quarkus-websockets-next`. It does NOT implement the Jakarta WebSocket spec; similarly named annotations behave differently.

## Endpoint basics

```java
@WebSocket(path = "/chat/{username}")
public class ChatWebSocket {
    @Inject WebSocketConnection connection;

    @OnOpen(broadcast = true)
    public ChatMessage onOpen() { ... connection.pathParam("username") ... }

    @OnTextMessage
    public ChatMessage onMessage(ChatMessage m) { return m; }

    @OnClose
    public void onClose() { connection.broadcast().sendTextAndAwait(departure); }
}
```

- Endpoints are CDI beans, `@Singleton` by default; singleton and `@ApplicationScoped` endpoints are shared across connections, so keep them stateless or thread-safe. `@SessionScoped` gives one instance per connection.
- Path is relative to `quarkus.http.root-path`. Path params are strings via `connection.pathParam(name)` or a `@PathParam String` callback parameter (unknown name fails the build). Query parameters are not supported; use `handshakeRequest().query()`.
- Nested static `@WebSocket` classes concatenate paths and inherit outer path params.

## Callback rules

At most one each of `@OnTextMessage`, `@OnBinaryMessage`, `@OnPingMessage`, `@OnPongMessage`, `@OnOpen`, `@OnClose`; any number of `@OnError`. An endpoint needs at least a message callback or `@OnOpen`. Violations fail the build. `@OnClose` may take `CloseReason`.

Message methods take exactly one message parameter (an object, or `Multi<X>`), plus optionally `WebSocketConnection`, `HandshakeRequest` and `@PathParam String`.

## Return types and threading

- `void` or object `X`: blocking; `X` is serialized and sent (returning `null` skips the reply).
- `Uni<Void>`, `Uni<X>`, `Multi<X>`: non-blocking, Quarkus subscribes. A failure or cancel closes the connection.
- `@Blocking`, `@RunOnVirtualThread`, `@Transactional` force blocking; `@NonBlocking` forces non-blocking.
- With a `Multi<X>` parameter, returning a derived `Multi` needs no subscription; returning `void` means you must subscribe, or no data is consumed.
- `@OnClose` on a server cannot return items to the client; use `connection.broadcast()`.

## Serialization and errors

`String`, `JsonObject`, `JsonArray`, `Buffer`, `byte[]` pass through; other types are JSON by default. A custom codec is a CDI bean implementing `TextMessageCodec` or `BinaryMessageCodec`; select with `@OnTextMessage(codec = ..., outputCodec = ...)`.

`@OnError` takes one `Throwable`-assignable parameter; the most specific type wins, and endpoint handlers beat global ones. Unhandled failures follow `quarkus.websockets-next.server.unhandled-failure-strategy`: log and close by default.

## Operations

- Events are processed serially by default; `InboundProcessingMode.CONCURRENT` drops ordering.
- `quarkus.websockets-next.server.max-pending-messages` defaults to `256`; `0` or negative disables the limit.
- `quarkus.websockets-next.server.auto-ping-interval=2` sends pings every 2 seconds.
- `quarkus.websockets-next.server.traffic-logging.enabled=true` plus DEBUG on `io.quarkus.websockets.next.traffic` logs traffic.
- `OpenConnections.listAll()` snapshots open connections.

## Checked

2026-11-07. Matched against the text (with includes) of: websockets-next-reference.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
