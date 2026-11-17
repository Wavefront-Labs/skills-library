---
id: computing-software.software-engineering.ktor.ktor-server-engines
name: ktor-server-engines
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, engines, netty, cio, enginemain, embeddedserver]
level: intro
status: docs-checked
description: "Pick a Ktor server engine (Netty, Jetty, Tomcat, CIO), add its artifact, and start it with embeddedServer or EngineMain, including createServer() and the Gradle main class."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-engines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choose and start a Ktor server engine

Server configuration includes an engine that processes network requests, host and port, and SSL settings.

## Supported engines

| Engine | Platforms | HTTP/2 |
|---|---|---|
| `Netty` | JVM | yes |
| `Jetty` | JVM | yes |
| `Tomcat` | JVM | yes |
| `CIO` | JVM, Native, GraalVM, JavaScript, WasmJs | no |
| `ServletApplicationEngine` | JVM | yes |

## Dependencies

Add one of: `ktor-server-netty`, `ktor-server-jetty-jakarta`, `ktor-server-tomcat-jakarta`, `ktor-server-cio`.

## embeddedServer

Pass an engine factory and parameters in code:

```kotlin
fun main() {
    embeddedServer(Netty, port = 8080) {
        // module code
    }.start(wait = true)
}
```

## EngineMain

Loads configuration from `application.conf` or `application.yaml`, including the application modules. Engine classes:

- `io.ktor.server.netty.EngineMain`
- `io.ktor.server.jetty.jakarta.EngineMain`
- `io.ktor.server.tomcat.jakarta.EngineMain`
- `io.ktor.server.cio.EngineMain`

To start through a build task, set the main class, for example in Gradle (Kotlin):

```kotlin
application {
    mainClass.set("io.ktor.server.netty.EngineMain")
}
```

Groovy uses `mainClassName = "io.ktor.server.netty.EngineMain"`; Maven uses a `main.class` property.

## Create without starting

`EngineMain.createServer(args)` returns an `EmbeddedServer` without starting it, so you can run initialization, logging or instrumentation first:

```kotlin
val server = io.ktor.server.netty.EngineMain.createServer(args)
server.start(wait = true)
```

Engine-specific options are set either in code (embeddedServer) or in the configuration file (EngineMain).

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-engines.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
