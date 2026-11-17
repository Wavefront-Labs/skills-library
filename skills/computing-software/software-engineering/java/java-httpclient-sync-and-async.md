---
id: computing-software.software-engineering.java.java-httpclient-sync-and-async
name: java-httpclient-sync-and-async
category: computing-software
field: software-engineering
product: java
tags: [java, java-networking, java-httpclient, java-net-http, http2, bodyhandlers, sendasync, http-timeouts]
level: practitioner
status: docs-checked
description: "Use java.net.http.HttpClient (Java 11+): one shared client, defaults, send vs sendAsync, body handlers, cancellation, closing the client (Java 21)."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.net.http/java/net/http/HttpClient.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# java.net.http.HttpClient

## Build once, share
```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(5))
    .followRedirects(HttpClient.Redirect.NORMAL)
    .build();
```
A built client is immutable and can send many requests. It manages its own connection pools and they are typically not shared between instances, so creating a client per operation usually prevents connection reuse. Share one.

Defaults (`newHttpClient()` is `newBuilder().build()`): HTTP/2 preferred (falls back to HTTP/1.1 where a constraint such as a proxy requires it), redirect policy `NEVER` (so set `followRedirects` if you expect redirects), the default proxy selector and default SSL context. System-wide defaults are read when the client is built; changing `ProxySelector` or `SSLContext` defaults later has no effect on existing clients. Other builder options: `proxy`, `authenticator`, `sslContext`, `executor`, `cookieHandler`.

## Requests
```java
HttpRequest req = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/items"))
    .timeout(Duration.ofSeconds(10))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofFile(Paths.get("file.json")))
    .build();
HttpResponse<String> res = client.send(req, HttpResponse.BodyHandlers.ofString());
if (res.statusCode() / 100 != 2) throw new IOException("HTTP " + res.statusCode());
```
A `BodyHandler` is required for every request and decides what the body becomes (`ofString` yields a `String`). Check `statusCode()` yourself. `send` blocks and throws `IOException` and `InterruptedException`; re-assert the interrupt if you catch it.

## Async
```java
client.sendAsync(req, HttpResponse.BodyHandlers.ofString())
      .thenApply(HttpResponse::body)
      .thenAccept(System.out::println);
```
`sendAsync` returns a `CompletableFuture<HttpResponse<T>>` at once; it completes exceptionally with `IOException` (or `SecurityException` under a security manager). Futures from the default implementation are cancelable: `cancel(true)` attempts to cancel the exchange, with no guarantee of timing, and the request may still reach the server. Cancelling may close an HTTP/1.1 connection abruptly or reset an HTTP/2 stream.

## Closing (Java 21)
`HttpClient` is `AutoCloseable` since 21. `close()` waits for submitted requests to finish and accepts no new ones; `shutdown()` does not wait; `shutdownNow()` tries to stop immediately; `awaitTermination(Duration)` waits. Streams from `ofInputStream()`, `ofLines()` or `ofPublisher()` that are not closed, cancelled or read to exhaustion may stop requests completing and stall a shutdown.

## Gotchas
- Non-2xx responses are not exceptions.
- Always close or fully read stream-returning body handlers.
- Test timeouts, 500s and redirects against a local stub server.

## Checked

Date: 2026-11-08

Read in full: the Java SE 21 HttpClient class Javadoc. Confirmed: immutability, connection-pool sharing, defaults (HTTP/2 preference, NEVER redirects), send and sendAsync semantics, exceptions, cancellation notes, shutdown and close methods (since 21) and the stream-handler warning. Removed because that page does not state them: the dev.java source (404), BodyHandler/BodyPublisher lists beyond those shown, the meaning of connect and request timeouts, the HTTPS-to-HTTP redirect rule, the restricted-headers and logging system properties, and virtual-thread executor advice.

Method: documentation only; no commands were run.
