---
id: computing-software.software-engineering.ktor.ktor-sessions
name: ktor-sessions
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, sessions, kotlin, cookie, storage, encryption, state]
level: advanced
status: docs-checked
description: "Configure the Ktor Sessions plugin: cookie or header transport, client or server payload, memory/directory/custom storage, signing and encryption, get/set/clear."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-sessions.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/session-cookie-client/src/main/kotlin/cookieclient/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/session-cookie-server/src/main/kotlin/com/example/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/session-header-server/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sessions in Ktor Server

The `Sessions` plugin (artifact `io.ktor:ktor-server-sessions`, `install(Sessions)`) persists data between HTTP requests: a logged-in user ID, a basket, preferences.

## Configuration choices

1. **Data class** per session, e.g. `UserSession`; several sessions need several classes.
2. **Transport.** Cookies suit HTML apps; headers suit APIs.
   - `cookie<UserSession>("user_session") { ... }` sets the cookie name; attributes such as path and expiration go in the block. For attributes not exposed, use `cookie.extensions["SameSite"] = "lax"`. Set `secure = true` before production.
   - `header<CartSession>("cart_session")`. With CORS add `allowHeader("cart_session")` and `exposeHeader("cart_session")`.
   - `sendOnlyIfModified = true` stops sending unchanged data (default sends on every response).
3. **Where the payload lives.** Passing only the name sends the whole payload to the client, so sign and encrypt it. Or store it on the server and pass only an ID:
   - `SessionStorageMemory`: development only, lost on restart.
   - `directorySessionStorage` writes files under a directory.
   - Custom: implement `SessionStorage` with suspending `invalidate(id)`, `write(id, value)`, `read(id)`.
4. **Protect data.**
   - Sign only: `transform(SessionTransportTransformerMessageAuthentication(signKey))` (default `HmacSHA256`); users can read but not alter.
   - Sign and encrypt: `SessionTransportTransformerEncrypt` (defaults `AES` and `HmacSHA256`). Since Ktor 3.0.0 the encryption method changed; set `backwardCompatibleRead` to read old sessions.
   - Never hard-code keys: use a config group fed by environment variables.

## Use

Full cookie-based example (signed and encrypted payload sent to the client):

```kotlin
@Serializable
data class UserSession(val id: String, val count: Int)

fun Application.main() {
    install(Sessions) {
        val secretEncryptKey = "00112233445566778899aabbccddeeff".hexToByteArray()
        val secretSignKey = "6819b57a326945c1968f45236589".hexToByteArray()
        cookie<UserSession>("user_session") {
            cookie.path = "/"
            cookie.maxAgeInSeconds = 10
            transform(SessionTransportTransformerEncrypt(secretEncryptKey, secretSignKey))
        }
    }
    routing {
        get("/login") {
            call.sessions.set(UserSession(id = "123abc", count = 0))
            call.respondRedirect("/user")
        }

        get("/user") {
            val userSession = call.sessions.get<UserSession>()
            if (userSession != null) {
                call.sessions.set(userSession.copy(count = userSession.count + 1))
                call.respondText("Session ID is ${userSession.id}. Reload count is ${userSession.count}.")
            } else {
                call.respondText("Session doesn't exist or is expired.")
            }
        }

        get("/logout") {
            call.sessions.clear<UserSession>()
            call.respondRedirect("/user")
        }
    }
}
```

Server-side storage, signed only (cookie with in-memory storage; for the header transport the example uses `directorySessionStorage(File("build/.sessions"))`):

```kotlin
install(Sessions) {
    val secretSignKey = "6819b57a326945c1968f45236589".hexToByteArray()
    cookie<CartSession>("cart_session", SessionStorageMemory()) {
        cookie.path = "/"
        transform(SessionTransportTransformerMessageAuthentication(secretSignKey))
    }
}
// header variant
install(Sessions) {
    header<CartSession>("cart_session", directorySessionStorage(File("build/.sessions"))) {
        transform(SessionTransportTransformerMessageAuthentication(secretSignKey))
    }
}
```

With `@Serializable data class CartSession(val userID: String, val productIDs: MutableList<Int>)`. Modify a session via the data class `copy`, as `/user` does above.

## Deferred loading

By default Ktor reads the session on every request that carries one. Set `System.setProperty("io.ktor.server.sessions.deferred", "true")` to defer loading, useful with costly custom storage.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-sessions.md, codeSnippets/snippets/session-cookie-client/src/main/kotlin/cookieclient/Application.kt, codeSnippets/snippets/session-cookie-server/src/main/kotlin/com/example/Application.kt, codeSnippets/snippets/session-header-server/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
