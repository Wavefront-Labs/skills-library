---
id: computing-software.web-development.gin.gin-health-checks
name: gin-health-checks
category: computing-software
field: web-development
product: gin
tags: [gin, health-check, liveness, readiness, healthz, readyz, kubernetes, probe]
level: practitioner
status: docs-checked
description: "Add Gin liveness /healthz and readiness /readyz endpoints that ping the database, with Kubernetes probe YAML and a timeout-guarded multi-dependency checker."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/health-check.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin health checks

Goal: let load balancers, Kubernetes and monitors verify the app is alive (liveness) and ready to serve (readiness).

- Liveness probe: is the process alive? If it fails, the container is restarted.
- Readiness probe: ready for traffic? If it fails, traffic is temporarily stopped but the container is not restarted.

```go
var isReady atomic.Bool

r.GET("/healthz", func(c *gin.Context) {
  c.JSON(http.StatusOK, gin.H{"status": "alive"})
})

r.GET("/readyz", func(c *gin.Context) {
  if !isReady.Load() {
    c.JSON(http.StatusServiceUnavailable, gin.H{"status": "not ready"})
    return
  }
  if err := db.Ping(); err != nil {
    c.JSON(http.StatusServiceUnavailable, gin.H{
      "status": "not ready",
      "reason": "database unreachable",
    })
    return
  }
  c.JSON(http.StatusOK, gin.H{"status": "ready"})
})

// Mark as ready after initialization is complete
isReady.Store(true)
```

Kubernetes probes:

```yaml
livenessProbe:
  httpGet: { path: /healthz, port: 8080 }
  initialDelaySeconds: 5
  periodSeconds: 10
readinessProbe:
  httpGet: { path: /readyz, port: 8080 }
  initialDelaySeconds: 5
  periodSeconds: 5
```

## Multiple dependencies
Derive a context with `context.WithTimeout(c.Request.Context(), 2*time.Second)`, then call `h.DB.PingContext(ctx)` and `h.Redis.Ping(ctx).Err()`; record each as healthy or unhealthy in a `gin.H`, and answer `http.StatusServiceUnavailable` if any failed, otherwise `http.StatusOK`.

## Test
```sh
curl -i http://localhost:8080/healthz
curl -i http://localhost:8080/readyz
# HTTP/1.1 200 OK
# {"status":"ready"}
```

## Gotcha
Always set a timeout on health check handlers: a hanging database connection should not block the check indefinitely; return unhealthy instead.

## Checked

2026-11-07. Every claim was matched line by line against the Gin website docs source (gin-gonic/website, src/content/docs/en/docs), read in full, including code samples: Health Checks (liveness vs readiness, atomic.Bool, Kubernetes probes, multi-dependency checker, timeout note).
Removed or corrected: nothing.

Method: documentation only; no commands were run.
