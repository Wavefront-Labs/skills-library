---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prom-client-nodejs-metrics
name: prom-client-nodejs-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, prom-client-usage, nodejs-metrics, nodejs, express, event-loop-lag, cluster-mode]
level: practitioner
status: verified
description: "Instrument Node.js with prom-client: default metrics (event loop lag, heap), Express middleware with route labels, cluster-mode aggregation, and async collect()."
sources: ["https://github.com/siimon/prom-client"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# prom-client for Node.js

```js
const client = require('prom-client');
const register = new client.Registry();
client.collectDefaultMetrics({ register, labels: { service: 'checkout' } });   // heap, GC, event loop lag, handles

const httpDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP latency',
  labelNames: ['method', 'route', 'code'],
  buckets: [0.05, 0.1, 0.3, 0.5, 1, 2, 5],
  registers: [register],
});

app.use((req, res, next) => {
  const end = httpDuration.startTimer();
  res.on('finish', () => end({ method: req.method, route: req.route?.path ?? 'unmatched', code: res.statusCode }));
  next();
});

app.get('/metrics', async (_req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());                 // metrics() is async in current versions
});
```
- `req.route.path` is the template (`/orders/:id`) only after routing; for unmatched routes use a constant.
- Key default metrics: `nodejs_eventloop_lag_p99_seconds`, `nodejs_heap_size_used_bytes`,
  `nodejs_gc_duration_seconds`, `process_cpu_seconds_total`.

## Values at scrape time
```js
new client.Gauge({ name: 'queue_depth', help: 'Jobs waiting', registers: [register],
  async collect() { this.set(await queue.count()); } });
```

## Cluster mode (node:cluster / PM2)
Each worker has its own registry. Use `AggregatorRegistry` in the primary:
```js
const aggregatorRegistry = new client.AggregatorRegistry();
// primary process HTTP server:
res.end(await aggregatorRegistry.clusterMetrics());
```
Workers must also construct `new client.AggregatorRegistry()` (the constructor installs the worker-side message listener; without
it `clusterMetrics()` rejects with `Operation timed out.`). Aggregation reads the default global registry; for other registries call
`client.AggregatorRegistry.setRegistries(registry)`. Custom metrics are summed by default (`aggregator` option: sum, first, min, max,
average, omit). In Kubernetes, prefer one process per container instead.

## Gotchas
- Creating a metric with the same name twice throws `A metric with the name ... has already been registered`
  (common with hot reload/tests: use `register.clear()` or a singleton module).
- Exemplars: create the metric with `enableExemplars: true`, then `httpDuration.observe({ labels, value, exemplarLabels: { traceId } })`
  and `register.setContentType(client.openMetricsContentType)`. Without `enableExemplars` that call object is read as a label set and
  throws `Added label "labels" is not included in initial labelset`.

## Verify
- [ ] `/metrics` shows `nodejs_eventloop_lag_seconds` and histogram buckets with route templates.
- [ ] Under cluster mode, counter values are the sum across workers and monotonic.

## Checked
Environment: Windows 11, Node.js 20.20.2, prom-client 15.1.3, express 5.3.0 (installed in a scratch folder).
- The first code block ran as written inside an Express app (plus a request to `/orders/5` and an unmatched path): content type `text/plain; version=0.0.4; charset=utf-8`; `http_request_duration_seconds_count` had `route="/orders/:id"` and `route="unmatched"`; default metrics carried `service="checkout"`; `nodejs_eventloop_lag_p99_seconds`, `nodejs_heap_size_used_bytes`, `process_cpu_seconds_total` present; `nodejs_gc_duration_seconds` is declared.
- The `collect()` gauge returned 7; a second `new client.Gauge` with the same name threw `A metric with the name queue_depth has already been registered.`
- Cluster mode: three `cluster.fork()` workers each with a Counter incremented by 2 and a Gauge set to 1: `clusterMetrics()` returned `wk_total 6` and `wk_gauge 3` when workers constructed an `AggregatorRegistry`, and rejected with `Operation timed out.` when they did not. `AggregatorRegistry.setRegistries` and the aggregator names come from the prom-client README.
- Exemplars: OpenMetrics output `exh_bucket{le="2"} 1 # {traceId="abc"} 1.5 ...` with `enableExemplars: true`; the error above without it. `client.openMetricsContentType` exists.
