---
id: computing-software.web-development.gin.gin-cookies
name: gin-cookies
category: computing-software
field: web-development
product: gin
tags: [gin, cookie, setcookie, setcookiedata, httponly, samesite, secure, maxage]
level: practitioner
status: docs-checked
description: "Set, read and delete cookies in Gin with c.SetCookie, c.Cookie and c.SetCookieData (v1.11+), with Secure, HttpOnly and SameSite guidance."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/cookie.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin cookies

Goal: set, read and delete HTTP cookies.

Signature:

```go
c.SetCookie(name, value string, maxAge int, path, domain string, secure, httpOnly bool)
```

- `maxAge`: seconds. `-1` deletes the cookie; `0` makes a session cookie (deleted when the browser closes).
- `path`: `"/"` makes it site-wide. `domain`: e.g. `"example.com"`, or `"localhost"` in development.
- `secure`: true sends only over HTTPS; set true in production.
- `httpOnly`: true hides it from `document.cookie` (helps against XSS); set true in production.

Set and get:

```go
router.GET("/cookie", func(c *gin.Context) {
  cookie, err := c.Cookie("gin_cookie")
  if err != nil {
    cookie = "NotSet"
    c.SetCookie("gin_cookie", "test", 3600, "/", "localhost", false, true)
  }
  fmt.Printf("Cookie value: %s \n", cookie)
})
```

```bash
curl -v http://localhost:8080/cookie
# Look for "Set-Cookie: gin_cookie=test" in the response headers
curl -v --cookie "gin_cookie=test" http://localhost:8080/cookie
# Server logs: Cookie value: test
```

Delete: `c.SetCookie("gin_cookie", "test", -1, "/", "localhost", false, true)`.

## http.Cookie (v1.11+)
`c.SetCookieData(&http.Cookie{...})` exposes `Expires`, `MaxAge`, `SameSite` and `Partitioned`:

```go
c.SetCookieData(&http.Cookie{
  Name: "session_id", Value: "abc123", Path: "/", Domain: "localhost",
  Expires: time.Now().Add(24 * time.Hour), MaxAge: 86400,
  Secure: true, HttpOnly: true, SameSite: http.SameSiteLaxMode,
  // Partitioned: true, // Go 1.22+
})
```

## Gotcha
For production the page recommends Secure true, HttpOnly true and SameSite Strict (or Lax) to limit CSRF and XSS exposure.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Cookie (SetCookie signature and parameter semantics, Cookie, delete with -1, SetCookieData v1.11+, production tip).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
