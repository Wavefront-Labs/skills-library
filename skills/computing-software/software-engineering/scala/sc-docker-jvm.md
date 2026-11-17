---
id: computing-software.software-engineering.scala.sc-docker-jvm
name: sc-docker-jvm
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-containers, docker-jvm]
level: practitioner
status: draft
description: "Build small, correct container images for Scala services and tune the JVM for containers."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Containerising Scala applications
- sbt-native-packager `sbt Docker/publishLocal` generates a Dockerfile; or use sbt-assembly plus a minimal JRE base image.
- The JVM respects container memory limits; size the heap with `-XX:MaxRAMPercentage=75`.
- Run as a non-root user; handle SIGTERM through a JVM shutdown hook or the effect system's graceful shutdown.
- Layer dependencies separately from application classes for cache-friendly builds.
Verify: `docker run -m 512m` and watch memory with `jcmd`.
