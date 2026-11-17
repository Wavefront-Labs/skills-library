---
id: computing-software.software-engineering.ktor.ktor-client-bearer-auth
name: ktor-client-bearer-auth
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, kotlin, http-client, bearer, oauth, auth, token-refresh]
level: advanced
status: docs-checked
description: "Configure Ktor client bearer authentication: loadTokens, refreshTokens, sendWithoutRequest, cacheTokens, markAsRefreshTokenRequest, with the OAuth 2.0 Google flow."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/client-bearer-auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bearer authentication in the Ktor client

Requires `io.ktor:ktor-client-auth`. Install the `Auth` plugin and configure the `bearer` provider:

```kotlin
val client = HttpClient(CIO) {
    install(Auth) {
        bearer {
            loadTokens { BearerTokens("abc123", "xyz111") }   // access, refresh
        }
    }
}
```

This sends `Authorization: Bearer abc123`.

## Callbacks

- `loadTokens {}`: supplies the initial access and refresh tokens as `BearerTokens`, typically from local storage.
- `refreshTokens {}`: runs when the access token is invalid. Receiver is `RefreshTokensParams`, giving `client`, `oldTokens` and `markAsRefreshTokenRequest()`. Return a new `BearerTokens`.
- `sendWithoutRequest { request -> ... }`: by default credentials go out only after a `401 Unauthorized`; return true to attach them up front, e.g. `request.url.host == "www.googleapis.com"`.
- `cacheTokens`: set `false` to call `loadTokens {}` for every request (useful when tokens change often).

## Refresh flow

1. A request with an invalid token gets `401 Unauthorized`.
2. The client invokes `refreshTokens {}`.
3. The request is retried with the new token.

If several requests get 401 at once, the refresh runs only once; the others wait and are retried with the new token.

With several auth providers installed, the response needs a `WWW-Authenticate` header. With only one provider, Ktor tries it for any 401 even without that header.

## Avoid refresh loops

Inside `refreshTokens {}`, call `markAsRefreshTokenRequest()` on the token request. Marked requests are excluded from the authentication retry mechanism, so a 401 on the refresh request itself does not trigger another refresh.

## Google OAuth example outline

1. Build the authorization URL with `client_id`, `scope`, `response_type=code`, `redirect_uri` (loopback `http://127.0.0.1:8080`, which needs a local listener) and `access_type=offline`.
2. Exchange the returned code for tokens by submitting form parameters; install `ContentNegotiation` with JSON to deserialize the token response.
3. Store tokens (a mutable list of `BearerTokens`) before creating the client, since the client config reads it.
4. On refresh, use the `refresh_token` grant type instead of `authorization_code`, save the new tokens, and read 401 error bodies as a typed error class.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/client-bearer-auth.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
