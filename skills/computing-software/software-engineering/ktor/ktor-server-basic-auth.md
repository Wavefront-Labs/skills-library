---
id: computing-software.software-engineering.ktor.ktor-server-basic-auth
name: ktor-server-basic-auth
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, basic-auth, authentication, kotlin, http, userhashedtableauth]
level: intro
status: docs-checked
description: "Protect Ktor Server routes with HTTP Basic authentication: realm, validate, UserIdPrincipal, UserHashedTableAuth for hashed passwords, and the type-safe basic scheme."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-basic-auth.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-basic/src/main/kotlin/authbasic/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-basic-hash-table/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic authentication in Ktor Server

Basic auth sends the username and password Base64-encoded in the `Authorization` header. It is effectively clear text, so serve it over HTTPS/TLS only. Dependency: `io.ktor:ktor-server-auth`.

## Flow

1. Client requests a route with no `Authorization` header.
2. Server answers `401` with `WWW-Authenticate: Basic realm="Access to the '/' path", charset="UTF-8"`. Ktor lets you set the realm and charset on the provider.
3. Client retries with `Authorization: Basic <base64 user:password>`.
4. Server validates and responds with the content.

## Configure

```kotlin
fun Application.main() {
    install(Authentication) {
        basic("auth-basic") {
            realm = "Access to the '/' path"
            validate { credentials ->
                val isValid = credentials.name == "jetbrains" &&
                    credentials.password == "foobar"
                if (isValid) {
                    UserIdPrincipal(credentials.name)
                } else {
                    null
                }
            }
        }
    }
    routing {
        authenticate("auth-basic") {
            get("/") {
                val user = call.principal<UserIdPrincipal>()
                call.respondText("Hello, ${user?.name}!")
            }
        }
    }
}
```

`validate` receives a `UserPasswordCredential` and returns a `UserIdPrincipal` on success or `null` on failure. Protect routes with `authenticate` and read the user via `call.principal<UserIdPrincipal>()`.

## Hashed passwords with UserHashedTableAuth

To avoid keeping plain passwords in an in-memory table:

1. Build a digest function with `getDigestFunction` (algorithm plus salt provider).
2. Create `UserHashedTableAuth`, setting `table` (usernames to hashed passwords) and `digester`.
3. In `validate`, call `UserHashedTableAuth.authenticate(credentials)`, which returns a `UserIdPrincipal` if the credentials are valid.

```kotlin
val digestFunction = getDigestFunction("SHA-256") {
    "ktor${it.length}"
}
val hashedUserTable = UserHashedTableAuth(
    table = mapOf(
        "jetbrains" to digestFunction("foobar"),
        "admin" to digestFunction("password")
    ),
    digester = digestFunction
)

install(Authentication) {
    basic("auth-basic-hashed") {
        realm = "Access to the '/' path"
        validate { credentials ->
            hashedUserTable.authenticate(credentials)
        }
    }
}
```

## Type-safe variant (experimental)

The `basic()` function creates a scheme for a principal type of your choice, with no `install(Authentication)` step; the scheme is a value you pass to the routes that need it. Inside `authenticateWith`, `call.principal` is your principal type and never `null`.

```kotlin
data class User(val name: String)

val basicAuth = basic<User>("auth-basic") {
    realm = "Access to the '/' path"
    validate { credentials ->
        val isValid = credentials.name == "jetbrains" &&
            credentials.password == "foobar"
        if (isValid) User(credentials.name) else null
    }
}

routing {
    authenticateWith(basicAuth) {
        get("/") {
            call.respondText("Hello, ${call.principal.name}!")
        }
    }
}
```

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-basic-auth.md, codeSnippets/snippets/auth-basic/src/main/kotlin/authbasic/Application.kt, codeSnippets/snippets/auth-basic-hash-table/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
