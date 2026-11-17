---
id: computing-software.software-engineering.scala.sc-logging-config
name: sc-logging-config
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-logging-config, logging-config]
level: practitioner
status: draft
description: "Configure logging with SLF4J and Logback and load configuration with Typesafe Config or pureconfig."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SLF4J logging and Typesafe Config
- Use scala-logging or the SLF4J API with Logback/log4j2; `logger.info(s"x=$x")` with scala-logging's macro avoids building the string when disabled.
- Typesafe Config: `ConfigFactory.load()` reads `application.conf` with `reference.conf` defaults; environment overrides through `${?ENV_VAR}`.
- pureconfig or ciris decode config to case classes with errors rather than exceptions.
- Do not log secrets.
Verify: change the log level via config and see the output change.
