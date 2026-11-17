---
id: computing-software.software-engineering.ktor.ktor-server-jwt-auth
name: ktor-server-jwt-auth
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, jwt, authentication, kotlin, hs256, rs256, bearer]
level: practitioner
status: docs-checked
description: "Authenticate Ktor Server clients with JSON Web Tokens: HS256 or RS256 setup, issuing a token at /login, verifier, required validate, challenge, and JWTPrincipal."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-jwt.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-jwt-hs256/src/main/kotlin/com/example/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-jwt-rs256/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWT authentication in Ktor Server

Ktor reads JWTs from the `Authorization` header (`Bearer` scheme), verifies the signature, and lets you validate the payload. Tokens are signed with a shared secret (`HS256`) or a key pair (`RS256`). Not supported on Kotlin/Native servers.

## Dependencies

```kotlin
implementation("io.ktor:ktor-server-auth:$ktor_version")
implementation("io.ktor:ktor-server-auth-jwt:$ktor_version")
```

## Flow

1. Client POSTs credentials (JSON) to a login route.
2. If valid, server builds a token with `JWT.create()` (auth0 `JWTCreator.Builder`), adds claims such as a custom `username`, signs it, and responds with it.
3. Client calls protected routes with `Authorization: Bearer <token>`.
4. Server verifies the signature and validates the payload.

## Configure

Keep JWT settings (secret, issuer, audience, realm) in a `jwt` group in the configuration file; do not store secrets as plain text, use environment variables.

application.conf (HS256):

```
jwt {
    secret = "secret"
    issuer = "http://0.0.0.0:8080/"
    audience = "http://0.0.0.0:8080/hello"
    realm = "Access to 'hello'"
}
```

HS256 setup (`@Serializable data class User(val username: String, val password: String)` is the login body):

```kotlin
val jwtConfig = environment.config
val secret = jwtConfig.property("jwt.secret").getString()
val issuer = jwtConfig.property("jwt.issuer").getString()
val audience = jwtConfig.property("jwt.audience").getString()
val myRealm = jwtConfig.property("jwt.realm").getString()
install(Authentication) {
    jwt("auth-jwt") {
        realm = myRealm
        verifier(JWT
                .require(Algorithm.HMAC256(secret))
                .withAudience(audience)
                .withIssuer(issuer)
                .build())
        validate { credential ->
            val payload = credential.payload
            val claim = payload.getClaim("username")
            if (claim.asString() != "") {
                JWTPrincipal(credential.payload)
            } else {
                null
            }
        }
        challenge { defaultScheme, realm ->
            val text = "Token is not valid or has expired"
            val status = HttpStatusCode.Unauthorized
            call.respond(status, text)
        }
    }
}
```

RS256 differs in the verifier, which takes a `JwkProvider`:

```kotlin
val jwkProvider = JwkProviderBuilder(issuer)
    .cached(10, 24, TimeUnit.HOURS)
    .rateLimited(10, 1, TimeUnit.MINUTES)
    .build()
// inside jwt("auth-jwt") { ... }
verifier(jwkProvider, issuer) {
    acceptLeeway(3)
}
```

- `realm` goes into `WWW-Authenticate`.
- `verifier`: for HS256 pass a `JWTVerifier`; for RS256 pass a `JwkProvider` pointing at a JWKS endpoint (for an issuer `http://0.0.0.0:8080` that is `http://0.0.0.0:8080/.well-known/jwks.json`).
- `validate` is required: without it provider initialization throws `IllegalArgumentException`. It gets a `JWTCredential` and returns `JWTPrincipal` or `null`.
- `challenge` customizes the failure response.

## Protect routes

Issue a token (HS256) and read claims and expiry from the principal:

```kotlin
routing {
    post("/login") {
        val user = call.receive<User>()
        // Check username and password
        // ...
        val expiresAt = System.currentTimeMillis() + 60000
        val token = JWT.create()
            .withAudience(audience)
            .withIssuer(issuer)
            .withClaim("username", user.username)
            .withExpiresAt(Date(expiresAt))
            .sign(Algorithm.HMAC256(secret))
        call.respond(hashMapOf("token" to token))
    }

    authenticate("auth-jwt") {
        get("/hello") {
            val principal = call.principal<JWTPrincipal>()
            val payload = principal!!.payload
            val username = payload.getClaim("username").asString()
            val now = System.currentTimeMillis()
            val expiresAt = principal.expiresAt?.time?.minus(now)
            call.respondText("Hello, $username! Token is expired at $expiresAt ms.")
        }
    }
}
```

For RS256 the login route builds `Algorithm.RSA256(publicKey as RSAPublicKey, privateKey as RSAPrivateKey)` (public key from `jwkProvider.get(keyId).publicKey`, private key decoded from the base64 PKCS8 `jwt.privateKey` setting) and signs with it; the example also serves `staticFiles(".well-known", File("certs"), "jwks.json")` as the JWKS endpoint.

Type-safe variant (experimental): the scheme reads claims in `validate` and returns your own type; the failure handler is `onUnauthorized` instead of `challenge`:

```kotlin
data class User(val username: String, val expiresAt: Long?)

val jwtAuth = jwt<User>("auth-jwt") {
    realm = myRealm
    verifier(JWT.require(Algorithm.HMAC256(secret)).withAudience(audience).withIssuer(issuer).build())
    validate { credential ->
        val username = credential.payload.getClaim("username").asString()
        if (username != "") User(username, credential.expiresAt?.time) else null
    }
    onUnauthorized = {
        call.respond(HttpStatusCode.Unauthorized, "Token is not valid or has expired")
    }
}

routing {
    authenticateWith(jwtAuth) {
        get("/hello") {
            val user = call.principal
            val expiresIn = user.expiresAt?.minus(System.currentTimeMillis())
            call.respondText("Hello, ${user.username}! Token is expired at $expiresIn ms.")
        }
    }
}
```

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-jwt.md, codeSnippets/snippets/auth-jwt-hs256/src/main/kotlin/com/example/Application.kt, codeSnippets/snippets/auth-jwt-rs256/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
