---
id: computing-software.software-engineering.ktor.ktor-cors
name: ktor-cors
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, cors, cross-origin, preflight, http-headers, kotlin-server]
level: practitioner
status: docs-checked
description: "Configure the Ktor CORS plugin: allowed hosts, methods, headers, exposed headers, credentials and preflight max age for cross-origin requests."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-cors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure CORS in a Ktor server

Install the `CORS` plugin (artifact `io.ktor:ktor-server-cors`) when your server must answer cross-origin requests, for example a browser client on another port calling `fetch('http://0.0.0.0:8080/customer')`. All settings live on `CORSConfig`.

## Hosts

```kotlin
install(CORS) {
    allowHost("client-host")
    allowHost("client-host:8081")
    allowHost("client-host", subDomains = listOf("en", "de", "es"))
    allowHost("client-host", schemes = listOf("http", "https"))
}
```

Use `anyHost()` to allow every origin.

## Methods

Only `GET`, `POST` and `HEAD` are allowed by default. Add others with `allowMethod(HttpMethod.Options)`, `HttpMethod.Put`, `HttpMethod.Patch`, `HttpMethod.Delete`.

## Headers

Default allowed client headers (`Access-Control-Allow-Headers`) are `Accept`, `Accept-Language` and `Content-Language`. Add more with `allowHeader(HttpHeaders.ContentType)` and `allowHeader(HttpHeaders.Authorization)`. For custom headers use `allowHeaders` or `allowHeadersPrefixed("custom-")`.

Gotcha: `allowHeaders` and `allowHeadersPrefixed` require the `allowNonSimpleContentTypes` property set to `true` for non-simple content types.

## Expose headers, credentials, preflight cache

- `exposeHeader("X-My-Custom-Header")` adds to `Access-Control-Expose-Headers`, the allowlist JavaScript in browsers can read.
- Browsers omit cookies and auth info on cross-origin requests by default; set `allowCredentials = true` to send `Access-Control-Allow-Credentials: true`.
- `maxAgeInSeconds = 3600` sets how long a preflight response may be cached before another preflight is needed.

## Route-level install

If you install `CORS` on a specific route rather than the application, add an `options` handler to that route so Ktor can answer the CORS preflight request correctly.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-cors.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
