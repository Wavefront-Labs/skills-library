---
id: computing-software.software-engineering.ktor.ktor-server-ldap-auth
name: ktor-server-ldap-auth
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, ldap, authentication, kotlin, directory, ldapauthenticate]
level: practitioner
status: docs-checked
description: "Authenticate users against an LDAP server in Ktor by calling ldapAuthenticate inside validate of a basic, digest or form provider, with optional extra checks."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-ldap.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-ldap/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP authentication in Ktor Server

LDAP is a protocol for directory services that can hold user information. Ktor authenticates LDAP users through the `basic`, `digest` or `form` providers: those collect the username and password, and you validate them against LDAP. Not supported on Kotlin/Native servers.

## Dependencies

```kotlin
implementation("io.ktor:ktor-server-auth:$ktor_version")
implementation("io.ktor:ktor-server-auth-ldap:$ktor_version")
```

## Configure

1. Pick a provider and call it inside `install(Authentication)`; import `io.ktor.server.auth.ldap.*`.
2. In its `validate` block, call `ldapAuthenticate(credentials, url, userDNFormat)`. It takes the `UserPasswordCredential` and checks it against the given server.

```kotlin
install(Authentication) {
    basic("auth-ldap") {
        validate { credentials ->
            val url = "ldap://0.0.0.0:389"
            val userDNFormat = "cn=%s,dc=ktor,dc=io"
            ldapAuthenticate(credentials, url, userDNFormat)
        }
    }
}
```

`validate` returns a `UserIdPrincipal` on success or `null` on failure. Optionally, add extra validation for an authenticated user with a trailing block (the page's sample check):

```kotlin
ldapAuthenticate(credentials, url, userDNFormat) {
    if (it.name == it.password) {
        UserIdPrincipal(it.name)
    } else {
        null
    }
}
```

3. Protect routes and read the user from `call.principal<UserIdPrincipal>()`:

```kotlin
routing {
    authenticate("auth-ldap") {
        get("/") {
            val user = call.principal<UserIdPrincipal>()
            call.respondText("Hello, ${user?.name}!")
        }
    }
}
```

## Type-safe variant (experimental)

There is no LDAP-specific type-safe scheme. Call `ldapAuthenticate` inside the `validate` block of a type-safe `basic<User>`, `digest` or `form` scheme, returning your own type from the block, then use `authenticateWith(ldapAuth)`:

```kotlin
data class User(val name: String)

val ldapAuth = basic<User>("auth-ldap") {
    validate { credentials ->
        val url = "ldap://0.0.0.0:389"
        val userDNFormat = "cn=%s,dc=ktor,dc=io"
        ldapAuthenticate(credentials, url, userDNFormat) {
            User(it.name)
        }
    }
}

routing {
    authenticateWith(ldapAuth) {
        get("/") {
            call.respondText("Hello, ${call.principal.name}!")
        }
    }
}
```

## Gotcha

The current LDAP implementation is synchronous.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-ldap.md, codeSnippets/snippets/auth-ldap/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
