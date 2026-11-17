---
id: computing-software.software-engineering.scala.sc-http-clients-sttp-http4s
name: sc-http-clients-sttp-http4s
category: computing-software
field: software-engineering
product: scala
tags: [scala, http-clients-sttp-http4s]
level: practitioner
status: draft
description: "Choose and use a Scala HTTP stack: sttp client, http4s servers, or java.net.http, with timeouts and JSON bodies."
sources: ["https://docs.scala-lang.org/scala3/book/introduction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HTTP stacks
- sttp: `basicRequest.get(uri"https://host/path").send(backend)` (confirm sttp 4 API); backends for JDK, Netty, http4s.
- http4s: `HttpRoutes.of[IO] { case GET -> Root / "ping" => Ok("pong") }` with Ember server.
- Always set connection and read timeouts, limit response body size, and decode via circe or upickle.
Verify: call the route with curl and assert the status.
