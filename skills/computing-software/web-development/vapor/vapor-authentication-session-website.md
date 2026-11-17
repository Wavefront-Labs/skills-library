---
id: computing-software.web-development.vapor.vapor-authentication-session-website
name: vapor-authentication-session-website
category: computing-software
field: web-development
product: vapor
tags: [vapor, authenticatable, sessions, sessionauthenticatable, login-form, redirectmiddleware, guardmiddleware, website]
level: advanced
status: docs-checked
description: "Persist Vapor logins in sessions with SessionAuthenticatable, ModelSessionAuthenticatable, RedirectMiddleware and a ModelCredentialsAuthenticatable form login."
sources:
  - https://docs.vapor.codes/security/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: browser-friendly auth where a session cookie keeps the user logged in. For APIs the docs recommend stateless tokens instead.

## SessionAuthenticatable
```swift
extension User: SessionAuthenticatable {
    var sessionID: String { self.email }   // must uniquely identify the user
}
struct UserSessionAuthenticator: AsyncSessionAuthenticator {
    typealias User = App.User
    func authenticate(sessionID: String, for request: Request) async throws {
        request.auth.login(User(email: sessionID))
    }
}
```
In practice use the id for a DB or API lookup. Combine session and an initial authenticator, order matters:
```swift
let protected = app.routes.grouped([
    app.sessions.middleware,
    UserSessionAuthenticator(),
    UserBearerAuthenticator(),
    User.guardMiddleware(),
])
```
Sessions middleware first; the session authenticator logs in if a session exists, otherwise the request falls to the next authenticator; the guard throws if none authenticated. After the first successful auth the response sets a cookie (e.g. `cookie: vapor_session=123`) that authenticates later requests.

## Fluent models
Empty conformance `extension User: ModelSessionAuthenticatable { }` uses the model id as session id and restores it from the DB. `User.sessionAuthenticator()` uses the default database; `User.sessionAuthenticator(.sqlite)` picks one.

## Website setup
Apply sessions and the session authenticator to every route that needs the user, including public pages and login routes; globally in configure.swift:
```swift
app.middleware.use(app.sessions.middleware)
app.middleware.use(User.sessionAuthenticator())
```
Note: the session cookie is not `secure` and `httpOnly` by default; see the Sessions docs for configuration.

## Redirect instead of 401
```swift
let protectedRoutes = app.grouped(User.redirectMiddleware(path: "/login?loginRequired=true"))
// or computed:
let redirectMiddleware = User.redirectMiddleware { req -> String in
    "/login?authRequired=true&next=\(req.url.path)"
}
let protectedRoutes = app.grouped([User.sessionAuthenticator(), redirectMiddleware])
```
Put the session authenticator before the redirect middleware.

## Form login
```swift
extension User: ModelCredentialsAuthenticatable {
    static let usernameKey = \User.$email
    static let passwordHashKey = \User.$password
    func verify(password: String) throws -> Bool {
        try Bcrypt.verify(password, created: self.password)
    }
}
let credentialsProtectedRoute = sessionRoutes.grouped(User.credentialsAuthenticator())
credentialsProtectedRoute.post("login", use: loginPostHandler)
```
The form POST must send fields named `username` and `password`. The authenticator finds the user, verifies the password, and the session authenticator then persists the login. Already conforming to `ModelAuthenticatable` is enough.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) security/authentication, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
