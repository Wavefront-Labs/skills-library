---
id: computing-software.software-engineering.scala.sc-scala-web-frontends
name: sc-scala-web-frontends
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-web-frontends, scala-web-frontends]
level: advanced
status: draft
description: "Choose between Scala.js frontends (Laminar) and server-rendered Play for a full-stack Scala web app."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Laminar, Play and full-stack Scala
- Laminar is a reactive UI library for Scala.js built on streams (`Var`, `Signal`, `EventStream`).
- Share case classes between a JVM backend and a JS frontend via crossProject, with JSON codecs derived once.
- Play Framework offers routes files, actions and templates with sbt integration.
- Serve the `fullLinkJS` bundle in production.
Verify: the JS bundle loads and talks to the backend in a browser test.
