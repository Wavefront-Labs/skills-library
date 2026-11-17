---
id: computing-software.software-engineering.java.spring-sse-and-websocket-endpoints
name: spring-sse-and-websocket-endpoints
category: computing-software
field: software-engineering
product: java
tags: [java, spring-web, spring-sse-websocket, server-sent-events, sseemitter, websocket, stomp]
level: practitioner
status: docs-checked
description: "Push data from Spring MVC: SseEmitter server-sent events, when WebSocket is worth it, the upgrade handshake, proxies, timeouts and thread cost."
sources: ["https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-async.html#mvc-ann-async-sse", "https://docs.spring.io/spring-framework/reference/web/websocket.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSE and WebSocket in Spring

## Server-sent events (one-way, plain HTTP)
`SseEmitter` (a subclass of `ResponseBodyEmitter`) formats events according to the W3C SSE specification. Return it from a controller with the event-stream media type, keep a reference, and send from another thread.
```java
@GetMapping(path = "/events", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public SseEmitter handle() {
    SseEmitter emitter = new SseEmitter();
    // Save the emitter somewhere..
    return emitter;
}
// In some other thread
emitter.send("Hello once");
emitter.send("Hello again");
emitter.complete();   // done at some point
```
- Wrap an `SseEmitter` in a `ResponseEntity` (via `ResponseBodyEmitter`) to set status and headers.
- If a send throws `IOException` (for example the client went away), do not call `complete` or `completeWithError` yourself: the servlet container raises an `AsyncListener` error and Spring MVC calls `completeWithError`, then does a final ASYNC dispatch to resolve the exception and finish the request.
- Timeout: unless set explicitly the default async timeout depends on the Servlet container. You can set a timeout on the `SseEmitter` itself, or globally through `configureAsyncSupport` on `WebMvcConfigurer`.
- Writes remain blocking and run on a separate thread (unlike WebFlux, which uses non-blocking I/O and needs no extra thread per write). The default `AsyncTaskExecutor` is not suitable for production under load, so configure your own.
- To carry `ThreadLocal` context across threads, the docs point to Micrometer context propagation.

## WebSocket (two-way)
- A WebSocket (RFC 6455) is a full-duplex channel over one TCP connection, started by an HTTP request with `Upgrade: websocket`; the server answers `101 Switching Protocols`.
- Unlike HTTP there is usually one URL for the connect and all messages flow on that connection; the protocol gives messages no semantics, so client and server must agree (for example STOMP, negotiated through `Sec-WebSocket-Protocol`).
- Spring's Servlet-stack support covers raw WebSocket, SockJS fallback and STOMP.
- Choose it only when low latency, high frequency and high volume combine; for low volume, HTTP streaming or polling (including SSE) is simpler.

## Gotchas
- Behind a web server such as nginx, configure it to pass WebSocket upgrade requests through; check your cloud provider's WebSocket instructions.
- Restrictive proxies may drop the `Upgrade` header or close connections that look idle, so public-facing use is riskier than internal use.

## Verify
`curl -N` against the endpoint streams events (not covered by the cited pages, but a standard check).

## Checked
Read the async-requests page in full (SSE, ResponseBodyEmitter, configuration sections) and the WebSocket overview page; the API, SockJS and STOMP subpages are separate pages and were not read. Removed as unconfirmed: the STOMP broker configuration, allowed-origin and CORS claims, handshake authentication and channel interceptors, simple-broker versus relay advice, heartbeat intervals, nginx buffering header, EventSource Last-Event-ID behaviour, and the virtual-thread suggestion.
Method: docs-checked 2026-11-09 against the Spring Framework async requests and WebSocket overview pages.
