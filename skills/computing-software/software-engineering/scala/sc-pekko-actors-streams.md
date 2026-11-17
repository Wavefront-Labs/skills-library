---
id: computing-software.software-engineering.scala.sc-pekko-actors-streams
name: sc-pekko-actors-streams
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-akka-pekko, pekko-actors-streams]
level: advanced
status: draft
description: "Know the Akka-to-Apache-Pekko licence change and write typed actors and backpressured streams."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Typed actors and streams
- Akka moved to the BUSL licence from 2.7; Apache Pekko is the Apache-licensed fork at the same API (package `org.apache.pekko`).
- Typed actors: `Behaviors.receive { (ctx, msg) => ... Behaviors.same }`; messages are immutable, never share mutable state.
- `ActorSystem(guardian, "name")`; ask pattern for request/response with a timeout.
- Streams: `Source(1 to 10).map(_ * 2).runWith(Sink.foreach(println))`; backpressure is built in; `mapAsync(parallelism)(f)`.
- Supervision with `Behaviors.supervise(...).onFailure(SupervisorStrategy.restart)`.
Verify: `ActorTestKit` tests for actors.
