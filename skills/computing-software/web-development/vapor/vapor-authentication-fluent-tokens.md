---
id: computing-software.web-development.vapor.vapor-authentication-fluent-tokens
name: vapor-authentication-fluent-tokens
category: computing-software
field: web-development
product: vapor
tags: [vapor, authenticatable, modelauthenticatable, fluent, user-tokens, bcrypt, bearer-token, login]
level: advanced
status: docs-checked
description: "Build password login and bearer-token auth in Vapor with Fluent: ModelAuthenticatable User, UserToken with ModelTokenAuthenticatable, signup, login and a protected route."
sources:
  - https://docs.vapor.codes/security/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: signup, Basic-protected `POST /login` that returns a token, and Bearer-protected routes.

## User model and migration
`User: Model, Content` with schema `users`, fields `name`, `email`, `password_hash` (`@ID(key: .id) var id: UUID?`). Migration (`AsyncMigration`, name "CreateUser") creates `.id()`, the three `.required` string fields and `.unique(on: "email")`; revert deletes the table. Register with `app.migrations.add(User.Migration())`.
Tip from the docs: emails are case-insensitive, but `ModelAuthenticatable` compares case-sensitively; if you lowercase in model middleware, lowercase user input too.

## Signup
```swift
app.post("users") { req async throws -> User in
    try User.Create.validate(content: req)
    let create = try req.content.decode(User.Create.self)
    guard create.password == create.confirmPassword else {
        throw Abort(.badRequest, reason: "Passwords did not match")
    }
    let user = try User(name: create.name, email: create.email,
                        passwordHash: Bcrypt.hash(create.password))
    try await user.save(on: req.db)
    return user
}
```
`User.Create` is a `Content` (name, email, password, confirmPassword); optionally `Validatable` with `name: !.empty`, `email: .email`, `password: .count(8...)`.

## ModelAuthenticatable
```swift
extension User: ModelAuthenticatable {
    static let usernameKey = \User.$email
    static let passwordHashKey = \User.$passwordHash
    func verify(password: String) throws -> Bool {
        try Bcrypt.verify(password, created: self.passwordHash)
    }
}
let passwordProtected = app.grouped(User.authenticator())
```

## Token model
`UserToken: Model, Content`, schema `user_tokens`, `@Field(key: "value") var value: String`, `@Parent(key: "user_id") var user: User`. Migration: `.id()`, `value` string required, `user_id` uuid required `.references("users", "id")`, `.unique(on: "value")`; register it too.

```swift
extension User {
    func generateToken() throws -> UserToken {
        try .init(value: [UInt8].random(count: 16).base64, userID: self.requireID())
    }
}
passwordProtected.post("login") { req async throws -> UserToken in
    let user = try req.auth.require(User.self)
    let token = try user.generateToken()
    try await token.save(on: req.db)
    return token
}
```
Login request: `POST /login` with a Basic `Authorization` header.

## ModelTokenAuthenticatable
```swift
extension UserToken: ModelTokenAuthenticatable {
    static var valueKey: KeyPath<UserToken, Field<String>> { \.$value }
    static var userKey: KeyPath<UserToken, Parent<User>> { \.$user }
    var isValid: Bool { true }
}
let tokenProtected = app.grouped(UserToken.authenticator())
tokenProtected.get("me") { req -> User in try req.auth.require(User.self) }
```
If `isValid` is false the token is deleted and the user is not authenticated. Call with `Authorization: Bearer <token>`.

Related: vapor-authentication-basic-bearer.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) security/authentication, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
