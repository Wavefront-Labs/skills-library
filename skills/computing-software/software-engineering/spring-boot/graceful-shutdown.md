---
id: computing-software.software-engineering.spring-boot.graceful-shutdown
name: graceful-shutdown
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, graceful-shutdown, shutdown, timeout-per-shutdown-phase, tomcat, jetty, reactor-netty, sigterm]
level: intro
status: docs-checked
description: "Graceful shutdown of embedded web servers: default behaviour, the spring.lifecycle.timeout-per-shutdown-phase grace period, request rejection and server.shutdown=immediate."
sources:
  - https://docs.spring.io/spring-boot/reference/web/graceful-shutdown.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Graceful shutdown is enabled by default with all three embedded web servers (Jetty, Reactor Netty, Tomcat) and with reactive and servlet-based web applications. It occurs as part of closing the application context, in the earliest phase of stopping `SmartLifecycle` beans. A timeout provides a grace period in which existing requests may complete but no new requests are permitted.

Configure the grace period:
```yaml
spring:
  lifecycle:
    timeout-per-shutdown-phase: "20s"
```
IDE caveat: shutdown from an IDE may be immediate rather than graceful if it does not send a proper `SIGTERM`; check your IDE's documentation.

Rejecting requests: the exact mechanism varies by server. Implementations may stop accepting requests at the network layer, or return a response with a specific HTTP status code or header; persistent connections can change how requests stop being accepted. Jetty, Reactor Netty and Tomcat stop accepting new requests at the network layer. For specifics see the `shutDownGracefully` API documentation of `TomcatWebServer`, `NettyWebServer` and `JettyWebServer`.

Disable graceful shutdown:
```yaml
server:
  shutdown: "immediate"
```
With Kubernetes probes, readiness reports `REFUSING_TRAFFIC` during graceful shutdown (see actuator-health-groups-and-kubernetes-probes).

## Checked

2026-11-07

Read graceful-shutdown.adoc (docs-repo source of the cited Graceful Shutdown page) in full; it is short. The shutDownGracefully javadoc it links to was not read. The closing sentence about the readiness REFUSING_TRAFFIC state is not on this page; it was confirmed in the shutdown-phase table of endpoints.adoc (Graceful shutdown row: Liveness CORRECT, Readiness REFUSING_TRAFFIC, new requests rejected).
Confirmed: enabled by default for Jetty, Reactor Netty and Tomcat and for reactive and servlet applications; part of closing the context in the earliest phase of stopping SmartLifecycle beans; timeout as a grace period for existing requests with no new requests permitted; spring.lifecycle.timeout-per-shutdown-phase "20s" example; IDE SIGTERM caveat; rejection mechanism varies by server (network layer, status code or header, persistent connections) and Jetty, Reactor Netty and Tomcat stop accepting at the network layer; the TomcatWebServer / NettyWebServer / JettyWebServer pointers; server.shutdown "immediate".
Nothing trimmed.

Method: documentation only; no commands were run.
