---
id: computing-software.software-engineering.ktor.ktor-server-form-auth
name: ktor-server-form-auth
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, form-auth, authentication, kotlin, login-form, html]
level: intro
status: docs-checked
description: "Authenticate Ktor Server users from a web login form: userParamName, passwordParamName, validate, challenge, a protected post route, and the type-safe form scheme."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-form-based-auth.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-form-html-dsl/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Form-based authentication in Ktor Server

Form authentication collects credentials from a web form. Build the form with the HTML DSL or a JVM template engine (FreeMarker, Velocity, and so on). Credentials travel as clear text, so use HTTPS/TLS. Dependency: `io.ktor:ktor-server-auth`.

## Flow

1. An unauthenticated client requests a route.
2. The server returns an HTML page with a form asking for username and password.
3. The user submits; the client sends the form data to the server. You must tell Ktor which parameter names carry the username and password.
4. The server validates and responds with the content.

## Configure (named provider)

```kotlin
install(Authentication) {
    form("auth-form") {
        userParamName = "username"
        passwordParamName = "password"
        validate { credentials ->
            val isValid = credentials.name == "jetbrains" &&
                credentials.password == "foobar"
            if (isValid) {
                UserIdPrincipal(credentials.name)
            } else {
                null
            }
        }
        challenge {
            val message = "Credentials are not valid"
            val status = HttpStatusCode.Unauthorized
            call.respond(status, message)
        }
    }
}
```

- `userParamName` / `passwordParamName` name the form fields.
- `validate` checks a `UserPasswordCredential` and returns `UserIdPrincipal` on success, `null` on failure.
- `challenge` runs when authentication fails, for example redirecting to the login page or sending `UnauthorizedResponse`.

## Protect the submit route

Define a `post` route for the form target and put it inside `authenticate("auth-form") { post("/login") { ... } }`. Inside, `call.principal<UserIdPrincipal>()` gives the user name. The page's example also serves the form with the HTML DSL:

```kotlin
routing {
    authenticate("auth-form") {
        post("/login") {
            val user = call.principal<UserIdPrincipal>()
            call.respondText("Hello, ${user?.name}!")
        }
    }

    get("/login") {
        call.respondHtml {
            body {
                val urlEncoded = FormEncType.applicationXWwwFormUrlEncoded
                form(action = "/login", encType = urlEncoded, method = FormMethod.post) {
                    p {
                        +"Username:"
                        textInput(name = "username")
                    }
                    p {
                        +"Password:"
                        passwordInput(name = "password")
                    }
                    p {
                        submitInput() { value = "Login" }
                    }
                }
            }
        }
    }
}
```

You can reuse `UserHashedTableAuth` (see basic authentication) to validate against hashed passwords. To keep the user logged in, store the username in a cookie session on first login and authorize later requests with the `session` provider.

## Type-safe variant (experimental)

```kotlin
data class User(val name: String)

val formAuth = form<User>("auth-form") {
    usernameField = "username"
    passwordField = "password"
    validate { credentials ->
        val isValid = credentials.name == "jetbrains" &&
            credentials.password == "foobar"
        if (isValid) User(credentials.name) else null
    }
    onUnauthorized = {
        val message = "Credentials are not valid"
        call.respond(HttpStatusCode.Unauthorized, message)
    }
}
```

Names differ from the classic provider: `usernameField`/`passwordField` instead of `userParamName`/`passwordParamName`, and `onUnauthorized` instead of `challenge`. Use it in routing (`call.principal` is the principal type, never null):

```kotlin
routing {
    authenticateWith(formAuth) {
        post("/login") {
            call.respondText("Hello, ${call.principal.name}!")
        }
    }
}
```

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-form-based-auth.md, codeSnippets/snippets/auth-form-html-dsl/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
