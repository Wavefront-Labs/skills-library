---
id: computing-software.software-engineering.ktor.ktor-server-bearer-auth
name: ktor-server-bearer-auth
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, bearer-auth, authentication, kotlin, tokens, http]
level: intro
status: docs-checked
description: "Validate bearer tokens in Ktor Server with the bearer provider: realm, the authenticate function returning UserIdPrincipal, and the type-safe validate variant."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-bearer-auth.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-bearer/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bearer authentication in Ktor Server

Bearer authentication uses security tokens sent in the `Authorization` header with the `Bearer` scheme. It underlies OAuth and JWT, but you can supply your own token-checking logic. Use it only over HTTPS/TLS. Dependency: `io.ktor:ktor-server-auth`.

## Flow

1. After the user authenticates and authorizes access, the server returns an access token.
2. The client calls the protected resource with `Authorization: Bearer <token>`.
3. The server validates the token.
4. On success the server returns the resource.

## Install and configure (classic)

```kotlin
fun Application.main() {
    install(Authentication) {
        bearer("auth-bearer") {
            realm = "Access to the '/' path"
            authenticate { tokenCredential ->
                if (tokenCredential.token == "abc123") {
                    UserIdPrincipal("jetbrains")
                } else {
                    null
                }
            }
        }
    }
    routing {
        authenticate("auth-bearer") {
            get("/") {
                val user = call.principal<UserIdPrincipal>()
                call.respondText("Hello, ${user?.name}!")
            }
        }
    }
}
```

Request:

```http
GET http://localhost:8080/
Authorization: Bearer abc123
```

- `realm` is sent in the `WWW-Authenticate` header.
- `authenticate` checks the token and returns a `UserIdPrincipal` on success, `null` otherwise.

Protect routes with `authenticate` and read the user from `call.principal<UserIdPrincipal>()`. The provider name is optional.

## Type-safe variant (experimental)

```kotlin
data class User(val name: String)

val bearerAuth = bearer<User>("auth-bearer") {
    realm = "Access to the '/' path"
    validate { tokenCredential ->
        if (tokenCredential.token == "abc123") {
            User("jetbrains")
        } else {
            null
        }
    }
}

routing {
    authenticateWith(bearerAuth) {
        get("/") {
            call.respondText("Hello, ${call.principal.name}!")
        }
    }
}
```

Note the rename: the classic provider uses `authenticate`, the type-safe scheme uses `validate`. There is no `install(Authentication)` step; inside `authenticateWith` `call.principal` is never null. Set `authHeader` to read the token from somewhere other than `Authorization`, and `authSchemes` to accept schemes other than `Bearer`.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-bearer-auth.md, codeSnippets/snippets/auth-bearer/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
