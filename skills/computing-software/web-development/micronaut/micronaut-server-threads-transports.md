---
id: computing-software.web-development.micronaut.micronaut-server-threads-transports
name: micronaut-server-threads-transports
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, thread-pools, event-loop, native-transport, virtual-threads, executeon, netty]
level: advanced
status: docs-checked
description: "Tune the Micronaut Netty server: base server settings, native transports, event loop groups, the I/O thread pool, @ExecuteOn blocking offload, and virtual threads."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/threadPools.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/threadPools/atBlocking.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/threadPools/blockingOperations.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/threadPools/virtualThreads.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Server configuration, event loops and thread pools

## Basic settings
Options live in `NettyHttpServerConfiguration` (extends `HttpServerConfiguration`):
```yaml
micronaut:
  server:
    maxRequestSize: 1MB
    host: localhost        # default binds all interfaces; localhost = loopback only
    netty:
      maxHeaderSize: 500KB
      worker:
        threads: 8
      childOptions:
        autoRead: true
```
Netty beans are on by default; `netty.enabled=false` disables all Netty integration, `micronaut.server.netty.enabled=false` only the server. Behind a proxy, two off-by-default flags: `micronaut.server.http10-keep-alive: true` (keep an HTTP/1.0 keep-alive connection when the response length is known) and `micronaut.server.reject-unsupported-http-versions: true` (answer other HTTP major versions with `505 HTTP Version Not Supported`). Netty leak detection: `netty.resource-leak-detector-level` = `DISABLED` (default), `SIMPLE`, `PARANOID`, `ADVANCED`.

## Native transports
Add the Netty native runtime dependency for your platform (`netty-transport-native-kqueue` for macOS with classifier `osx-x86_64` or `osx-aarch_64`; `netty-transport-native-epoll` or `netty-transport-native-io_uring` for Linux with `linux-x86_64` or `linux-aarch_64`), group `io.netty`, scope `runtimeOnly`. Then:
```yaml
micronaut:
  netty:
    event-loops:
      default:
        transport: io_uring,epoll,kqueue,nio
```
The first available transport is used. Remove `nio` to guarantee native; an exception is thrown if none is available.

## Event loops
The worker uses the `default` event loop group, configured at `micronaut.netty.event-loops.default`. `micronaut.server.netty.worker` settings are only used when `event-loop-group` names a group that is not configured under `micronaut.netty.event-loops` (deprecated). The parent group is configured at `micronaut.server.netty.parent`. To use another group:
```yaml
micronaut:
  server:
    netty:
      worker:
        event-loop-group: other
  netty:
    event-loops:
      other:
        num-threads: 10
```
Default thread count is `io.netty.eventLoopThreads` or available processors x 2.

## Blocking work
Never block the event loop. The page recommends `@ExecuteOn` to run blocking operations on a different thread pool (for example `@ExecuteOn(TaskExecutors.BLOCKING)` on a controller); it works with both `MANUAL` (default since 2.0) and `AUTO` `micronaut.server.thread-selection`. `@Blocking` only offloads to the IO pool under `AUTO`. The `io` executor is an unbounded caching pool by default; resize it:
```yaml
micronaut:
  executors:
    io:
      type: fixed
      nThreads: 75
```

## Virtual threads
When the JVM supports virtual threads (Java 19 preview needs `--enable-preview`), the `blocking` executor uses them; otherwise it aliases to `io`. Experimental: run virtual threads on the event loop with JVM flag `--add-opens=java.base/java.lang=ALL-UNNAMED` and `micronaut.netty.event-loops.default.loom-carrier: true`. The page ties this experimental mode to Micronaut HTTP Server Netty 4.9.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against all five cited pages: the sample server YAML and its comments, Netty enable flags, the two HTTP/1.x flags, native transport dependencies and `transport` list, leak detector levels, event loop group rules and thread-count default, `@Blocking` versus `@ExecuteOn`, the `io` pool, and virtual threads including the loom carrier. Removed: the claim that WebSockets are annotated with `@ExecuteOn`, which these pages do not state.
