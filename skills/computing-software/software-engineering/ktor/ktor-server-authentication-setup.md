---
id: computing-software.software-engineering.ktor.ktor-server-authentication-setup
name: ktor-server-authentication-setup
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, authentication, kotlin, principal, credential, authenticate, provider]
level: practitioner
status: docs-checked
description: "Install the Ktor Server Authentication plugin, name providers, validate credentials into principals, protect routes with authenticate, and read call.principal."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-auth.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-basic/src/main/kotlin/authbasic/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-form-session/src/main/kotlin/com/example/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-form-session-nested/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting up Authentication in Ktor Server

The `Authentication` plugin (package `io.ktor.server.auth`, artifact `io.ktor:ktor-server-auth`) handles authentication and authorization. Some providers, such as JWT and LDAP, need extra artifacts.

## Steps

1. **Choose a provider** inside `install(Authentication) { ... }` by calling its function: `basic`, `digest`, `form`, `jwt`, `oauth`, `session`, or a custom `provider()`.
2. **Name it** (optional): `basic("auth-basic") { ... }` and `form("auth-form") { ... }`. Names must be unique, and you may define only one provider without a name.
3. **Configure it.** The key function is `validate()`: it checks a credential and returns a principal (any object) on success or `null` on failure.
   - A *principal* is the authenticated entity. `basic`, `digest` and `form` produce `UserIdPrincipal`; `jwt` produces `JWTPrincipal`. You can map to your own class, for example one that carries extra data or session data.
   - A *credential* is what the server checks: `UserPasswordCredential` for `basic` and `form`, `JWTCredential` for `jwt`.
   - Use `skipWhen { call -> ... }` to skip a provider on a condition, for example `call.sessions.get<UserSession>() != null`.
4. **Protect routes** with `authenticate("auth-basic") { get("/orders") { ... } }`. Routes outside the block stay public.
5. **Read the principal** in the handler with `call.principal<UserIdPrincipal>()`. For nested providers, pass the provider name: `call.principal<UserSession>("auth-session")`.

Docs example (`auth-basic`) covering steps 1-5:

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

With session authentication the principal is the session data class, so pass it to `call.principal`:

```kotlin
authenticate("auth-session") {
    get("/hello") {
        val userSession = call.principal<UserSession>()
        // ...
    }
}
```

## Nested providers and strategy

`authenticate` also takes a `strategy` (an `AuthenticationStrategy` value). With `AuthenticationStrategy.Required`, the client must pass every provider in the nest, so only a user that passed session authentication can try basic authentication for `/admin` (from the `auth-form-session-nested` example):

```kotlin
val required = AuthenticationStrategy.Required
authenticate("auth-session", strategy = required) {
    get("/hello") {
        val userSession = call.principal<UserSession>()
        // ...
    }
    authenticate("auth-basic", strategy = required) {
        get("/admin") {
            val userSession =
                call.principal<UserSession>(
                    "auth-session"
                )
            call.respondText(
                "Hi, ${userSession?.name}! " +
                    "Welcome to the Admin page."
            )
        }
    }
}
```

## Custom provider

`provider("custom")` registers a named provider that you apply with `authenticate("custom")`. The `authenticate {}` block runs for every incoming request:

```kotlin
provider("custom") {
  authenticate { context ->
    val headers = context.call.request.headers
    val exampleHeader = headers["Example-Header"]
    if (exampleHeader == null) {
      val message = "No example header found"
      val cause = AuthenticationFailedCause.Error(message)
      context.challenge(key = this, cause) { challenge, call ->
        call.respondText("Challenge")
        challenge.complete()
      }
    }
  }
}
```

Extra options live on `DynamicProviderConfig`.

## Notes

Ktor also has an experimental type-safe authentication scheme API (a separate topic) as an alternative to named providers; both can coexist in one application.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-auth.md, codeSnippets/snippets/auth-basic/src/main/kotlin/authbasic/Application.kt, codeSnippets/snippets/auth-form-session/src/main/kotlin/com/example/Application.kt, codeSnippets/snippets/auth-form-session-nested/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
