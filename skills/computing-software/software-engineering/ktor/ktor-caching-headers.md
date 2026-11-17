---
id: computing-software.software-engineering.ktor.ktor-caching-headers
name: ktor-caching-headers
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, caching, cache-control, expires, http-headers, kotlin-server]
level: practitioner
status: docs-checked
description: "Set Cache-Control and Expires headers in Ktor with the CachingHeaders plugin, per content type, per route, or per call via ApplicationCall.caching."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-caching-headers.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/caching-headers/src/main/kotlin/cachingheaders/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Set HTTP caching headers in Ktor

The `CachingHeaders` plugin (artifact `io.ktor:ktor-server-caching-headers`, package `io.ktor.server.plugins.cachingheaders`) configures `Cache-Control` and `Expires`. Settings can apply globally, to a route, or to a single call.

## Application level

Inside `install(CachingHeaders) { ... }` define the `options` function. It receives the `ApplicationCall` and the response content, and returns a `CachingOptions` (or null) so you can choose a strategy per content type. The docs example adds `Cache-Control` with `max-age` for plain text and HTML:

```kotlin
install(CachingHeaders) {
    options { call, content ->
        when (content.contentType?.withoutParameters()) {
            ContentType.Text.Plain -> CachingOptions(CacheControl.MaxAge(maxAgeSeconds = 3600))
            ContentType.Text.Html -> CachingOptions(CacheControl.MaxAge(maxAgeSeconds = 60))
            else -> null
        }
    }
}
```

`CachingOptions` takes two parameters:

- `cacheControl`: a `CacheControl` value. `CacheControl.MaxAge` sets `max-age` plus related settings such as visibility and revalidation options. `CacheControl.NoCache` or `CacheControl.NoStore` disable caching.
- `expires`: the `Expires` header as a `GMTDate` or `ZonedDateTime`.

## Route level

Plugins can be installed on specific routes, not just globally. Install `CachingHeaders` inside a route block (the docs example uses the `/index` route) to give only that route its caching header:

```kotlin
route("/index") {
    install(CachingHeaders) {
        options { call, content -> CachingOptions(CacheControl.MaxAge(maxAgeSeconds = 1800)) }
    }
    get {
        call.respondText("Index page")
    }
}
```

## Call level

For finer control, set caching options inside a handler through the `ApplicationCall.caching` property. The docs example picks different options depending on whether the user is logged in; for login you can use the Authentication and Sessions plugins.

```kotlin
get {
    val userLoggedIn = true
    if(userLoggedIn) {
        call.caching = CachingOptions(CacheControl.NoStore(CacheControl.Visibility.Private))
        call.respondText("Profile page")
    } else {
        call.caching = CachingOptions(CacheControl.MaxAge(maxAgeSeconds = 900))
        call.respondText("Login page")
    }
}
```

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-caching-headers.md, codeSnippets/snippets/caching-headers/src/main/kotlin/cachingheaders/Application.kt.

Removed or changed: removed the Related section (the ConditionalHeaders pairing is not on the page).

Method: documentation only; no commands were run.
