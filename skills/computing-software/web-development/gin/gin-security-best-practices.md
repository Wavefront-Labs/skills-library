---
id: computing-software.web-development.gin.gin-security-best-practices
name: gin-security-best-practices
category: computing-software
field: web-development
product: gin
tags: [gin, security, cors, csrf, rate-limiting, securejson, trusted-proxies, autotls, sql-injection]
level: practitioner
status: docs-checked
description: "Checklist for hardening a Gin app: gin-contrib cors and csrf, a x/time/rate limiter, binding validation, SecureJSON, SetTrustedProxies and autotls HTTPS."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/middleware/security-guide.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin security best practices

Goal: apply layered defences before production. No single technique is sufficient.

## CORS (gin-contrib/cors)
```go
r.Use(cors.New(cors.Config{
  AllowOrigins:     []string{"https://example.com"},
  AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
  AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
  ExposeHeaders:    []string{"Content-Length"},
  AllowCredentials: true,
  MaxAge:           12 * time.Hour,
}))
```
Never combine `AllowOrigins: []string{"*"}` with `AllowCredentials: true`.

## CSRF (gin-contrib/csrf)
Needed for state-changing endpoints that rely on cookie auth. Requires a session store first:
```go
store := cookie.NewStore([]byte("session-secret"))
r.Use(sessions.Sessions("mysession", store))
r.Use(csrf.Middleware(csrf.Options{
  Secret: "csrf-token-secret",
  ErrorFunc: func(c *gin.Context) {
    c.String(403, "CSRF token mismatch")
    c.Abort()
  },
}))
token := csrf.GetToken(c)
```
APIs using only `Authorization` headers (e.g. Bearer tokens) are not vulnerable to CSRF.

## Rate limiting
A per-IP map of `rate.NewLimiter(10, 20)` (10 requests/second, burst 20) from `golang.org/x/time/rate`, keyed on `c.ClientIP()` under a `sync.Mutex`; when `!cl.limiter.Allow()` call `c.AbortWithStatusJSON(http.StatusTooManyRequests, gin.H{"error": "rate limit exceeded"})`. In production add cleanup of stale entries and consider a Redis-backed limiter for multiple instances.

## Input validation and SQL
```go
type CreateUser struct {
  Username string `json:"username" binding:"required,alphanum,min=3,max=30"`
  Email    string `json:"email"    binding:"required,email"`
  Age      int    `json:"age"      binding:"required,gte=1,lte=130"`
}
if err := c.ShouldBindJSON(&req); err != nil { c.JSON(400, gin.H{"error": err.Error()}); return }
```
Use placeholders: `db.QueryRow("SELECT id FROM users WHERE username = $1", username)`, never string concatenation.

## XSS
Use `c.JSON` for structured data, `c.SecureJSON` (prepends `while(1);`), and `X-Content-Type-Options: nosniff`.

## Proxies and TLS
`router.SetTrustedProxies([]string{"10.0.0.1", "192.168.1.0/24"})` so forged `X-Forwarded-For` cannot bypass IP controls. HTTPS: `log.Fatal(autotls.Run(r, "example.com"))` from `github.com/gin-gonic/autotls`; pair with the HSTS header.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: middleware/security-guide.md. Confirmed: the cors.Config example and the wildcard-with-credentials warning, the csrf and sessions setup, the rate.NewLimiter(10, 20) per-IP limiter and 429 response, validation tags, parameterised queries, SecureJSON, nosniff, SetTrustedProxies, autotls.Run and HSTS advice. Trimmed nothing. Linked sub-pages (security headers, trusted proxies, Lets Encrypt) are covered by their own skills and were not relied on here.

Method: documentation only; no commands were run.
