---
id: computing-software.web-development.gin.gin-security-headers
name: gin-security-headers
category: computing-software
field: web-development
product: gin
tags: [gin, security, security-headers, csp, hsts, x-frame-options, host-header-injection, ginhelmet]
level: practitioner
status: docs-checked
description: "Add security headers (CSP, HSTS, X-Frame-Options, nosniff, Referrer-Policy, Permissions-Policy) in a Gin middleware and reject a wrong Host header, or use gin-helmet."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/middleware/security-headers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Security headers middleware in Gin

Goal: harden responses and avoid Host Header Injection (SSRF, open redirection).

```go
r := gin.Default()

expectedHost := "localhost:8080"

r.Use(func(c *gin.Context) {
  if c.Request.Host != expectedHost {
    c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{"error": "Invalid host header"})
    return
  }
  c.Header("X-Frame-Options", "DENY")
  c.Header("Content-Security-Policy", "default-src 'self'; connect-src *; font-src *; script-src-elem * 'unsafe-inline'; img-src * data:; style-src * 'unsafe-inline';")
  c.Header("X-XSS-Protection", "1; mode=block")
  c.Header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
  c.Header("Referrer-Policy", "strict-origin")
  c.Header("X-Content-Type-Options", "nosniff")
  c.Header("Permissions-Policy", "geolocation=(),midi=(),sync-xhr=(),microphone=(),camera=(),magnetometer=(),gyroscope=(),fullscreen=(self),payment=()")
  c.Next()
})
```

## What each header does (per the docs)
- `X-Content-Type-Options: nosniff`: stops MIME-type sniffing.
- `X-Frame-Options: DENY`: prevents clickjacking by blocking the page in an iframe.
- `Content-Security-Policy`: restricts where scripts, styles, images and fonts may load from; a strong XSS defence.
- `X-XSS-Protection: 1; mode=block`: largely deprecated (Chrome removed its XSS Auditor in 2019); defence in depth for older browsers.
- `Strict-Transport-Security`: forces HTTPS for the `max-age`; `includeSubDomains` extends to subdomains.
- `Referrer-Policy: strict-origin`: sends only the origin, only over HTTPS.
- `Permissions-Policy`: restricts browser features such as camera and microphone.

## Check it
```bash
curl localhost:8080/ping -I                    # headers present
curl localhost:8080/ping -I -H "Host:neti.ee"  # HTTP/1.1 400 Bad Request
```

## Alternative
`go get github.com/danielkov/gin-helmet/ginhelmet`, then `r.Use(ginhelmet.Default())` for default security headers.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: middleware/security-headers.md. Confirmed: the middleware code and every header value, the Host check returning 400, the per-header explanations (including X-XSS-Protection being largely deprecated), the curl checks and the ginhelmet alternative. Trimmed nothing. The gin-helmet repository was not opened.

Method: documentation only; no commands were run.
