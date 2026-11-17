---
id: computing-software.software-engineering.ktor.ktor-client-cookies
name: ktor-client-cookies
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, kotlin, http-client, cookies, httpcookies, session]
level: intro
status: docs-checked
description: "Keep cookies between Ktor client calls with the HttpCookies plugin, preset cookies with ConstantCookiesStorage, read them with client.cookies, or write a CookiesStorage."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/client-cookies.md
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/client-requests.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cookies in the Ktor client

## Manual handling

- `cookie()` in a request appends a cookie to that one request.
- `setCookie()` on a response parses the `Set-Cookie` header value.

## Automatic: HttpCookies

`HttpCookies` needs only `ktor-client-core`. It stores cookies and sends them on later calls; the default storage is in-memory.

```kotlin
val client = HttpClient(CIO) {
    install(HttpCookies)
}
```

Installing it is enough for the client to keep cookies between requests. Once installed, cookies added through `cookie()` on a request are ignored.

## Fixed cookies (useful in tests)

`ConstantCookiesStorage` adds a given set of cookies to every request for a domain:

```kotlin
val client = HttpClient(CIO) {
    install(HttpCookies) {
        storage = ConstantCookiesStorage(Cookie(name = "user_name", value = "jetbrains", domain = "0.0.0.0"))
    }
}
```

## Read stored cookies

`client.cookies("http://0.0.0.0:8080/")` returns the cookies stored for that URL.

## Persistent storage

Implement the `CookiesStorage` interface and assign it with `storage = CustomCookiesStorage()` in the `install(HttpCookies)` block. The page points to `AcceptAllCookiesStorage` as a reference to copy from.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/client-cookies.md, topics/client-requests.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages. Added client-requests.md to sources (it confirms that cookie() values are ignored when HttpCookies is installed).

Method: documentation only; no commands were run.
