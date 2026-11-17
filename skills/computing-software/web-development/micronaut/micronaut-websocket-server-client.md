---
id: computing-software.web-development.micronaut.micronaut-websocket-server-client
name: micronaut-websocket-server-client
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, websocket, server-websocket, client-websocket, broadcaster, onmessage, idle-timeout]
level: practitioner
status: docs-checked
description: "Build WebSocket servers with @ServerWebSocket and clients with @ClientWebSocket in Micronaut, including broadcasting, non-blocking handlers, scopes and timeouts."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/websocket.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/websocket/websocketServer.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/websocket/websocketClient.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Micronaut WebSockets

Since Micronaut 4.0 `micronaut-http-server` no longer brings WebSocket support transitively: add the `micronaut-websocket` dependency.

## Server
```java
@ServerWebSocket("/chat/{topic}/{username}")
@ExecuteOn(TaskExecutors.BLOCKING)
public class ChatServerWebSocket {
    private WebSocketBroadcaster broadcaster;
    public ChatServerWebSocket(WebSocketBroadcaster broadcaster) { this.broadcaster = broadcaster; }

    @OnOpen
    public void onOpen(String topic, String username, WebSocketSession session) {
        broadcaster.broadcastSync("[" + username + "] Joined!", isValid(topic, session));
    }

    @OnMessage
    public void onMessage(String topic, String username, String message, WebSocketSession session) {
        broadcaster.broadcastSync("[" + username + "] " + message, isValid(topic, session));
    }

    @OnClose
    public void onClose(String topic, String username, WebSocketSession session) {
        broadcaster.broadcastSync("[" + username + "] Disconnected!", isValid(topic, session));
    }

    private Predicate<WebSocketSession> isValid(String topic, WebSocketSession session) {
        return s -> s != session && topic.equalsIgnoreCase(s.getUriVariables().get("topic", String.class, null));
    }
}
```
- The URI can be a template; it sits under `micronaut.server.context-path` if set. Method arguments can be URI variables or a `WebSocketSession`.
- `@OnMessage` body types: Netty `WebSocketFrame`, simple types convertible from `ByteBuf` (e.g. `String`), `byte[]`/`ByteBuf`/`ByteBuffer`, a POJO (decoded as JSON by default; custom codec via `@Consumes`), or `WebSocketPongMessage` for pongs only.
- `@OnClose` may take a `CloseReason`; it runs before the session closes. `@OnError` may take the exception type; with no `@OnError`, an unrecoverable exception closes the socket.
- Callbacks run on the Netty event loop; use `@ExecuteOn` (type or method level) for blocking calls such as `broadcastSync`/`sendSync`.
- Non-blocking: return a `Publisher` or `Future` from handlers, e.g. `Publisher<Message> onMessage(...)` returning `broadcaster.broadcast(newMessage, predicate)`. Outside handlers use `broadcastAsync`/`sendAsync`.
- The instance is shared across all connections by default (synchronize state); annotate with `@Prototype` for one instance per connection.
- Adding the `session` module shares HTTP sessions with the WebSocket session.
- Idle connections time out after five minutes; change with `micronaut.server.idle-timeout` (e.g. `30m`, negative = no timeout). For the Micronaut client set `micronaut.http.client.read-idle-timeout`.

## Client
```java
@ClientWebSocket("/chat/{topic}/{username}")
public abstract class ChatClientWebSocket implements AutoCloseable {
    private WebSocketSession session;
    @OnOpen
    public void onOpen(String topic, String username, WebSocketSession session, HttpRequest request) {
        this.session = session;
    }
    @OnMessage
    public void onMessage(String message) { /* collect replies */ }

    public abstract void send(String message);                       // blocking
    public abstract Future<String> sendAsync(String message);        // future
    public abstract reactor.core.publisher.Mono<String> sendRx(String message); // reactive
}
```
Abstract methods starting with `send` or `broadcast` are implemented at compile time. Connect:
```java
@Inject @Client("http://localhost:8080") WebSocketClient webSocketClient;
ChatClientWebSocket chat = webSocketClient.connect(ChatClientWebSocket.class, "/chat/football/fred").blockFirst();
chat.send("Hello World!");
```
Close the client endpoint when done. `AsyncWebSocketClient.connect(...)` returns a `CompletionStage` instead (continuations must not block). Set `handshake-timeout` (`micronaut.http.client.handshake-timeout`) to fail a connect that never gets the upgrade response with a `ReadTimeoutException`; the default is no limit.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.
