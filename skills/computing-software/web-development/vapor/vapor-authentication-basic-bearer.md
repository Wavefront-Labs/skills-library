---
id: computing-software.web-development.vapor.vapor-authentication-basic-bearer
name: vapor-authentication-basic-bearer
category: computing-software
field: web-development
product: vapor
tags: [vapor, authenticatable, guardmiddleware, authentication, basic-auth, bearer-token, req-auth, middleware]
level: practitioner
status: docs-checked
description: "Authenticate Vapor requests with Authenticatable users, Basic and Bearer authenticators, req.auth, GuardMiddleware, and composed authenticators."
sources:
  - https://docs.vapor.codes/security/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: protect routes via the Authorization header.

An authenticator (middleware) holds the verification logic; on success it puts the user in `req.auth`, on failure it adds nothing (it does not reject). Base types: `RequestAuthenticator`, `BasicAuthenticator`, `BearerAuthenticator`, `CredentialsAuthenticator` (each with an `Async...` variant).

## User type
```swift
struct User: Authenticatable { var name: String }
```
(A struct, class or Fluent `Model`.)

## Protect a route
```swift
let protected = app.grouped(UserAuthenticator())
protected.get("me") { req -> String in
    try req.auth.require(User.self).name
}
```
`require` throws if not authenticated. Add `GuardMiddleware` to demand authentication: `.grouped(User.guardMiddleware())`.

## Basic
Header `Authorization: Basic <base64(user:pass)>`; never send over plaintext or unverified TLS. Typically used once to log in and mint a token.
```swift
struct UserAuthenticator: AsyncBasicAuthenticator {
    typealias User = App.User
    func authenticate(basic: BasicAuthorization, for request: Request) async throws {
        if basic.username == "test" && basic.password == "secret" {
            request.auth.login(User(name: "Vapor"))
        }
    }
}
```
Never store plaintext passwords; compare hashes. Failed credentials give 401 Unauthorized.

## Bearer
Header `Authorization: Bearer foo`.
```swift
struct UserAuthenticator: AsyncBearerAuthenticator {
    typealias User = App.User
    func authenticate(bearer: BearerAuthorization, for request: Request) async throws {
        if bearer.token == "foo" { request.auth.login(User(name: "Vapor")) }
    }
}
```
Real implementations look the token up in a database or verify cryptographically (as with JWT). Consider horizontal scalability.

## Composition
- Same user type: chain authenticators then guard, e.g. `app.grouped(UserPasswordAuthenticator()).grouped(UserTokenAuthenticator()).grouped(User.guardMiddleware())`.
- Different user types: chain both and check in the handler: `guard req.auth.has(Admin.self) || req.auth.has(User.self) else { throw Abort(.unauthorized) }`.

## Manual
`req.auth.login(user)`, `try req.auth.require(User.self)`, `req.auth.get(User.self)` (optional), `req.auth.logout(User.self)`. Useful for testing.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) security/authentication, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
