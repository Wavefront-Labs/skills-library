---
id: computing-software.software-engineering.ktor.ktor-client-engines
name: ktor-client-engines
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, kotlin, http-client, engines, multiplatform, cio, okhttp]
level: practitioner
status: docs-checked
description: "Choose and configure a Ktor client engine (CIO, Apache5, Java, Jetty, OkHttp, Android, Darwin, WinHttp, Curl, Js): platforms, dependencies, HTTP/2 and WebSocket support."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/client-engines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a Ktor client engine

The client is multiplatform; each platform needs an engine in addition to `ktor-client-core`. Pass the engine class to the constructor: `HttpClient(CIO)`. Configure it in an `engine { }` block (common options from `HttpClientEngineConfig`, plus engine-specific config).

## Engines and platforms

| Engine | Platforms | Artifact |
|---|---|---|
| `Apache5` | JVM | `ktor-client-apache5` |
| `Java` | JVM | `ktor-client-java` |
| `Jetty` | JVM | `ktor-client-jetty-jakarta` |
| `Android` | JVM, Android | `ktor-client-android` |
| `OkHttp` | JVM, Android | `ktor-client-okhttp` |
| `Darwin` | Native | `ktor-client-darwin` |
| `WinHttp` | Native | `ktor-client-winhttp` |
| `Curl` | Native | `ktor-client-curl` |
| `CIO` | JVM, Android, Native, JS, WasmJs | `ktor-client-cio` |
| `Js` | JavaScript | `ktor-client-js` |

Minimum versions: Apache5 Java 8+; Java and Jetty Java 11+; CIO Java 8+ and Android 7.0+ (older Android needs Java 8 API desugaring); OkHttp Android 5.0+.

## Selection rules

- Omit the engine (`HttpClient()`) and Ktor picks from the engine dependencies on the classpath. One available means that one; several means the highest priority. `CIO` has the lowest priority by default.
- For most Kotlin Multiplatform projects, add `api("io.ktor:ktor-client-engine-defaults:<version>")` to `commonMain` instead of per-platform engine dependencies.
- With Maven, platform suffixes such as `-jvm` must be written manually; Gradle resolves them.

## Engine notes

- `Apache5` supports HTTP/1.1 and HTTP/2 (HTTP/2 on by default) and is the recommended Apache engine; the older `Apache` engine (Apache HttpClient 4) is deprecated. In its config, use `configureConnectionManager` for connection settings such as max connections; use `customizeClient` only for unrelated settings (proxy, interceptors, logging).
- `Jetty` supports only HTTP/2. `CIO` supports only HTTP/1.x.
- `Darwin` uses `NSURLSession` (`configureRequest`, `configureSession`). `WinHttp` has `protocolVersion`. `Js` uses Fetch (node-fetch on Node.js) and accepts a custom `fetch` in `engine {}`.

## Limitations

HTTP/2: Apache5, Java, Jetty, OkHttp, Js, Darwin, WinHttp, Curl yes; CIO and Android no. WebSockets: Java, CIO, OkHttp, Js, Darwin, WinHttp, Curl yes; Apache5, Jetty, Android no. SSL must be configured per engine; some engines do not support proxies; `HttpTimeout` has engine limits.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/client-engines.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
