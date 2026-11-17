---
id: computing-software.web-development.gin.gin-trusted-proxies
name: gin-trusted-proxies
category: computing-software
field: web-development
product: gin
tags: [gin, trusted-proxies, settrustedproxies, clientip, trustedplatform, x-forwarded-for, cloudflare]
level: advanced
status: docs-checked
description: "Configure which proxies Gin trusts for ClientIP with Engine.SetTrustedProxies, disable it with nil, or set Engine.TrustedPlatform for CDNs."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/trusted-proxies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin trusted proxies

Goal: make `c.ClientIP()` return the real client address and resist forged forwarding headers.

Behind a reverse proxy (Nginx, HAProxy, a cloud load balancer) the client IP arrives in headers such as `X-Forwarded-For` or `X-Real-Ip`, but any client can set those. Without configuration an attacker can bypass IP-based access controls, poison logs and audit trails, and evade rate limiting keyed on `ClientIP()`.

`SetTrustedProxies` tells Gin which network addresses are legitimate proxies (IPv4/IPv6 addresses or CIDRs). `ClientIP()` then trusts only forwarding entries added by them; requests arriving directly from elsewhere use the raw remote address.

```go
router := gin.Default()
router.SetTrustedProxies([]string{"192.168.1.2"})

router.GET("/", func(c *gin.Context) {
  // If the client is 192.168.1.2, use the X-Forwarded-For header to
  // deduce the original client IP from the trustworthy parts of it.
  // Otherwise, simply return the direct client IP
  fmt.Printf("ClientIP: %s\n", c.ClientIP())
})
router.Run()
```

## No proxy
`Engine.SetTrustedProxies(nil)` disables the feature; `Context.ClientIP()` then returns the remote address directly, avoiding unnecessary computation.

## CDN / platform header
`Engine.TrustedPlatform` skips the TrustedProxies check and has higher priority:

```go
router.TrustedPlatform = gin.PlatformGoogleAppEngine
router.TrustedPlatform = gin.PlatformCloudflare
router.TrustedPlatform = gin.PlatformFlyIO
// or your own header, e.g. one your CDN sets:
router.TrustedPlatform = "X-CDN-Client-IP"
```

## Gotchas
- By default Gin trusts all proxies if you do not call `SetTrustedProxies`; the page says this is NOT safe.
- For a custom `TrustedPlatform` header, make sure your CDN prevents users from passing that header.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: server-config/trusted-proxies.md. Confirmed: why forged X-Forwarded-For matters, accepted address and CIDR forms, trust-all default being NOT safe, SetTrustedProxies(nil), TrustedPlatform priority and the three predefined platforms, and the custom header warning. Trimmed nothing.

Method: documentation only; no commands were run.
