---
id: computing-software.web-development.gin.gin-session-management
name: gin-session-management
category: computing-software
field: web-development
product: gin
tags: [gin, sessions, gin-contrib-sessions, cookie-store, redis, sessions-options, httponly, samesite]
level: practitioner
status: docs-checked
description: "Add sessions to Gin with gin-contrib/sessions: cookie or Redis store, sessions.Default(c) Set/Get/Clear/Save, sessions.Options, available backends, and sessions vs JWT."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/middleware/session-management.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Session management with gin-contrib/sessions

Goal: keep per-user data across requests. Install: `go get github.com/gin-contrib/sessions`.

## Cookie store
```go
store := cookie.NewStore([]byte("your-secret-key"))
r.Use(sessions.Sessions("mysession", store))

r.GET("/login", func(c *gin.Context) {
  session := sessions.Default(c)
  session.Set("user", "john")
  session.Save()
  c.JSON(http.StatusOK, gin.H{"message": "logged in"})
})

r.GET("/profile", func(c *gin.Context) {
  session := sessions.Default(c)
  user := session.Get("user")
  if user == nil {
    c.JSON(http.StatusUnauthorized, gin.H{"error": "not logged in"})
    return
  }
  c.JSON(http.StatusOK, gin.H{"user": user})
})

r.GET("/logout", func(c *gin.Context) {
  session := sessions.Default(c)
  session.Clear()
  session.Save()
})
```
Imports: `github.com/gin-contrib/sessions` and `github.com/gin-contrib/sessions/cookie`.

## Redis store
For multi-instance production use:
```go
store, err := redis.NewStore(10, "tcp", "localhost:6379", "", []byte("secret"))
if err != nil {
  panic(err)
}
r.Use(sessions.Sessions("mysession", store))
```
Import `github.com/gin-contrib/sessions/redis`.

## Options
```go
session.Options(sessions.Options{
  Path:     "/",
  MaxAge:   3600,
  HttpOnly: true,
  Secure:   true,
  SameSite: http.SameSiteLaxMode,
})
```
`Path` defaults to `/`. `MaxAge` is in seconds: `-1` deletes, `0` is a browser session. `SameSite` accepts Lax, Strict, None.

## Backends
Cookie (`sessions/cookie`), Redis (`sessions/redis`), Memcached (`sessions/memcached`), MongoDB (`sessions/mongo`), PostgreSQL (`sessions/postgres`).

## Sessions vs JWT
Sessions are server-side with easy revocation but need a shared store; JWT is client-side and stateless but hard to revoke (needs a blocklist). Use sessions for logout/ban; JWT for stateless auth across microservices.

## Gotchas
- The page's examples call `session.Save()` after `Set` and `Clear`.
- Set `HttpOnly: true` and `Secure: true` in production.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: middleware/session-management.md. Confirmed: install, cookie and Redis store code, the Options table (Path default /, MaxAge -1 and 0, SameSite values), the backend table and the sessions-versus-JWT comparison. Reworded one gotcha: the page shows session.Save() after Set and Clear but never says always, so the skill now says the examples do it.

Method: documentation only; no commands were run.
