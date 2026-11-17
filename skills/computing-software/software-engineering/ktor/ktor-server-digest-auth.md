---
id: computing-software.software-engineering.ktor.ktor-server-digest-auth
name: ktor-server-digest-auth
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, digest-auth, authentication, kotlin, rfc7616, hashing, qop]
level: advanced
status: docs-checked
description: "Configure RFC 7616 Digest authentication in Ktor Server: algorithms, HA1 digestProvider, QoP auth-int, userHashResolver, strictRfc7616Mode, and security advice."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-digest-auth.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-digest/src/main/kotlin/authdigest/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Digest authentication in Ktor Server

Digest hashes the credentials before sending, so passwords never travel in clear text. Ktor supports RFC 7616. Dependency: `io.ktor:ktor-server-auth`; the provider is not supported on Kotlin/Native servers. Still use HTTPS/TLS in production.

## Flow

The server replies `401` with `WWW-Authenticate: Digest realm=..., nonce=..., algorithm=..., qop="auth"`. The client answers with an `Authorization: Digest` header whose `response = H(HA1:nonce:nc:cnonce:qop:HA2)`, where `HA1 = H(username:realm:password)` and `HA2 = H(method:digestURI)` (or with the entity body hash for `auth-int`). The server stores `HA1`.

## Configure

```kotlin
val myRealm = "Access to the '/' path"
val userPasswords: Map<String, String> = mapOf(
    "jetbrains" to "foobar",
    "admin" to "password"
)

fun computeHash(userName: String, realm: String, password: String, algorithm: DigestAlgorithm): ByteArray =
    algorithm.toDigester().digest("$userName:$realm:$password".toByteArray(UTF_8))

fun Application.main() {
    install(Authentication) {
        digest("auth-digest") {
            realm = myRealm
            // Support both modern SHA-512-256 and legacy MD5 clients
            algorithms = listOf(DigestAlgorithm.SHA_512_256, DigestAlgorithm.MD5)
            digestProvider { userName, realm, algorithm ->
                // Compute H(username:realm:password) using the requested algorithm
                userPasswords[userName]?.let { password ->
                    computeHash(userName, realm, password, algorithm)
                }
            }
            validate { credentials ->
                if (credentials.userName.isNotEmpty()) {
                    CustomPrincipal(credentials.userName, credentials.realm)
                } else {
                    null
                }
            }
        }
    }
    routing {
        authenticate("auth-digest") {
            get("/") {
                val user = call.principal<CustomPrincipal>()
                call.respondText("Hello, ${user?.userName}!")
            }
        }
    }
}

data class CustomPrincipal(val userName: String, val realm: String)
```

- `algorithms`: constants `SHA_512_256`, `SHA_512_256_SESS`, `SHA_256`, `SHA_256_SESS` (recommended or good), `MD5`, `MD5_SESS` (deprecated, legacy only). Defaults are SHA-512-256 and MD5. With several, the server sends several `WWW-Authenticate` headers.
- `-sess` variants compute `H(H(username:realm:password):nonce:cnonce)`: resistant to precomputed attacks, but the server must hash on every request.
- `nonceManager` controls nonce generation; use a custom `NonceManager` for distributed deployments.
- `supportedQop = listOf(DigestQop.AUTH, DigestQop.AUTH_INT)` inside the `digest("auth-digest") { ... }` block; `AUTH` is the default. With `auth-int` the body is consumed, so install `DoubleReceive` if the handler needs it.

## Advanced options

- `userHashResolver { userhash, realm, algorithm -> username }` enables username hashing; the server then advertises `userhash=true`.
- `strictRfc7616Mode()` removes MD5 and enforces UTF-8.
- `charset = Charsets.UTF_8` is the default.
- On success with QoP the server returns `Authentication-Info` (`rspauth`, `nextnonce`, `qop`, `nc`, `cnonce`).

Protect routes with `authenticate("auth-digest") { ... }`. The type-safe `digest<T>()` scheme is JVM only.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-digest-auth.md, codeSnippets/snippets/auth-digest/src/main/kotlin/authdigest/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
