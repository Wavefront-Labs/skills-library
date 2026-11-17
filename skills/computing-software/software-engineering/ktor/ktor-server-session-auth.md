---
id: computing-software.software-engineering.ktor.ktor-server-session-auth
name: ktor-server-session-auth
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, session-auth, authentication, kotlin, cookie, sessions]
level: practitioner
status: docs-checked
description: "Authenticate returning Ktor users via the session provider: UserSession data class, cookie Sessions, validate and challenge, call.sessions.set after form login."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-session-auth.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-form-session/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Session authentication in Ktor Server

A user who already has an associated session can be authenticated with the `session` provider. The typical pattern: log in once with a web form, save the username in a cookie session, then authorize later requests from that session. Not supported on Kotlin/Native servers.

## Dependencies

Add both `io.ktor:ktor-server-sessions` and `io.ktor:ktor-server-auth`.

## Flow (with form login)

1. Client posts form data (username and password).
2. Server validates, saves the username to a cookie session, and responds with a cookie.
3. Client requests a protected resource with the cookie.
4. Ktor checks that a session exists for the cookie and optionally validates its data, then serves the content.

## Steps

1. **Data class** for session data:

```kotlin
@Serializable
data class UserSession(val name: String, val count: Int)
```

2. **Install Sessions** with a cookie for that class, setting a cookie path and expiration:

```kotlin
install(Sessions) {
    cookie<UserSession>("user_session") {
        cookie.path = "/"
        cookie.maxAgeInSeconds = 60
    }
}
```

3. **Install the provider** with the session type (alongside the `form("auth-form")` provider from the form-auth skill):

```kotlin
install(Authentication) {
    session<UserSession>("auth-session") {
        validate { session ->
            if(session.name.startsWith("jet")) {
                session
            } else {
                null
            }
        }
        challenge {
            call.respondRedirect("/login")
        }
    }
}
```

   `validate()` checks the session instance and returns a principal (type `Any`) on success. `challenge()` runs on failure: redirect to the login page or send an `UnauthorizedResponse`.
4. **Save the session at login:** in the form-authenticated route call `call.sessions.set(...)`:

```kotlin
authenticate("auth-form") {
    post("/login") {
        val principal = call.principal<UserIdPrincipal>()
        val userName = principal?.name.toString()
        val session = UserSession(name = userName, count = 1)
        call.sessions.set(session)
        call.respondRedirect("/hello")
    }
}
```

5. **Protect routes.** The principal is the session data class itself:

```kotlin
authenticate("auth-session") {
    get("/hello") {
        val userSession = call.principal<UserSession>()
        val next = userSession?.copy(count = userSession.count + 1)
        call.sessions.set(next)
        call.respondText("Hello, ${userSession?.name}! Visit count is ${userSession?.count}.")
    }
}
```

A type-safe session authentication scheme also exists; it gives non-null principals and read-write session access.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-session-auth.md, codeSnippets/snippets/auth-form-session/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
