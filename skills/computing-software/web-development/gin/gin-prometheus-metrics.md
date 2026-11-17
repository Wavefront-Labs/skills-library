---
id: computing-software.web-development.gin.gin-prometheus-metrics
name: gin-prometheus-metrics
category: computing-software
field: web-development
product: gin
tags: [gin, metrics, prometheus, openmetrics, promhttp, fullpath, client-golang, wraph]
level: practitioner
status: docs-checked
description: "Expose Prometheus metrics from Gin with gin-contrib/openmetrics or a custom counter and histogram middleware, using c.FullPath labels and a separate metrics port."
sources:
  - https://github.com/gin-gonic/website/blob/master/src/content/docs/en/docs/server-config/metrics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gin Prometheus metrics

Goal: expose request rate, latency and error metrics for Prometheus.

## Ready-made middleware
```sh
go get github.com/gin-contrib/openmetrics
```
```go
r := gin.Default()
// Expose /metrics endpoint for Prometheus scraping
r.Use(openmetrics.NewOpenMetrics("myapp", openmetrics.WithExpose()))
```

## Custom metrics with prometheus/client_golang
```go
httpRequestsTotal = prometheus.NewCounterVec(
  prometheus.CounterOpts{Name: "http_requests_total", Help: "Total number of HTTP requests"},
  []string{"method", "path", "status"},
)
httpRequestDuration = prometheus.NewHistogramVec(
  prometheus.HistogramOpts{
    Name: "http_request_duration_seconds", Help: "HTTP request duration in seconds",
    Buckets: prometheus.DefBuckets,
  },
  []string{"method", "path"},
)
// init(): prometheus.MustRegister(httpRequestsTotal); prometheus.MustRegister(httpRequestDuration)

func MetricsMiddleware() gin.HandlerFunc {
  return func(c *gin.Context) {
    start := time.Now()
    c.Next()
    duration := time.Since(start).Seconds()
    status := strconv.Itoa(c.Writer.Status())
    httpRequestsTotal.WithLabelValues(c.Request.Method, c.FullPath(), status).Inc()
    httpRequestDuration.WithLabelValues(c.Request.Method, c.FullPath()).Observe(duration)
  }
}

r.Use(MetricsMiddleware())
r.GET("/metrics", gin.WrapH(promhttp.Handler()))
```

## Separate port
Serve metrics internally while the app is public:

```go
go func() {
  metrics := http.NewServeMux()
  metrics.Handle("/metrics", promhttp.Handler())
  http.ListenAndServe(":9090", metrics)
}()
app.Run(":8080")
```

Prometheus scrape config:

```yaml
scrape_configs:
  - job_name: "gin-app"
    scrape_interval: 15s
    static_configs:
      - targets: ["localhost:9090"]
```

Check: `curl http://localhost:9090/metrics` should show lines such as `http_requests_total{method="GET",path="/ping",status="200"} 1`.

## Gotcha
Use `c.FullPath()` (e.g. `/user/:id`) rather than `c.Request.URL.Path` (`/user/123`) for the path label, to avoid high-cardinality labels that can overwhelm Prometheus.

## Checked

Checked: 2026-11-07.

Read in full from a local clone of the gin-gonic/website repository (markdown source, examples inline, no include files). Page read: server-config/metrics.md. Confirmed: the openmetrics install and NewOpenMetrics call, the counter and histogram definitions, MustRegister in init, the c.FullPath() label advice, the separate :9090 metrics server, the scrape config and the sample output line. Trimmed nothing. The linked openmetrics and client_golang repositories were not opened.

Method: documentation only; no commands were run.
