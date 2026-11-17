---
id: computing-software.web-development.gin.gin-basicauth-middleware
name: gin-basicauth-middleware
category: computing-software
field: web-development
product: gin
tags: [gin, basicauth, gin-accounts, gin-authuserkey, c-mustget, route-group, http-401]
level: intro
status: docs-checked
description: "Protect a Gin route group with gin.BasicAuth and a gin.Accounts map, read the user via gin.AuthUserKey, and test with curl -u."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/middleware/using-basicauth-middleware.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin BasicAuth middleware

Goal: require HTTP Basic credentials on a route group.

`gin.BasicAuth()` takes a `gin.Accounts` map (shortcut for `map[string]string`) of username to password.

```go
router := gin.Default()

authorized := router.Group("/admin", gin.BasicAuth(gin.Accounts{
  "foo":    "bar",
  "austin": "1234",
}))

authorized.GET("/secrets", func(c *gin.Context) {
  // set by the BasicAuth middleware
  user := c.MustGet(gin.AuthUserKey).(string)
  if secret, ok := secrets[user]; ok {
    c.JSON(http.StatusOK, gin.H{"user": user, "secret": secret})
  } else {
    c.JSON(http.StatusOK, gin.H{"user": user, "secret": "NO SECRET :("})
  }
})
router.Run(":8080")
```

Here `secrets` is a `gin.H` of per-user data you define yourself.

## Try it
```bash
curl -u foo:bar http://localhost:8080/admin/secrets          # authenticated
curl -u foo:wrongpassword http://localhost:8080/admin/secrets # 401 Unauthorized
curl http://localhost:8080/admin/secrets                      # 401 Unauthorized
```

## Gotchas
- Basic auth sends credentials Base64-encoded, not encrypted; always use HTTPS in production.
- The hardcoded accounts are for demonstration. Load real credentials from environment variables, a secrets manager, or a database with hashed passwords, and never commit plaintext credentials.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Using BasicAuth middleware (gin.Accounts, AuthUserKey, curl results, security notes).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
