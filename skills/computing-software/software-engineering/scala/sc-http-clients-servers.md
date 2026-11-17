---
id: computing-software.software-engineering.scala.sc-http-clients-servers
name: sc-http-clients-servers
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-http-db, http-clients-servers]
level: practitioner
status: draft
description: "Choose an HTTP client or server library, define endpoints once with Tapir and test them."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# sttp, http4s and Tapir
- sttp client: `basicRequest.get(uri"https://x.test/a?b=$b").send(backend)`; `uri""` interpolation escapes query parameters.
- http4s (functional, Cats Effect), Play, Pekko HTTP and Tapir (describe endpoints, derive server, client and OpenAPI) are the common server options.
- Always set timeouts and a bounded connection pool.
- Tests: `tapir` stub backends or http4s `Client.fromHttpApp`.
Verify: hit a local server in an integration test.
