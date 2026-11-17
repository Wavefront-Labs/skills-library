---
id: computing-software.web-development.node-express.health-check-endpoints
name: health-check-endpoints
category: computing-software
field: web-development
product: node-express
tags: [health-check-endpoint, liveness-probe, readiness-probe, graceful-shutdown, kubernetes-probes, node]
level: practitioner
status: verified
description: "Designing liveness and readiness endpoints for Node services: what each checks, dependency checks with timeouts, readiness during shutdown, probe settings and what not to expose."
sources:
  - https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
  - https://expressjs.com/en/advanced/healthcheck-graceful-shutdown.html
  - https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Health check endpoints

## 1. Two questions, two endpoints
| Endpoint | Question | Checks | Failure action |
|---|---|---|---|
| `/livez` (liveness) | is the process wedged? | event loop responds; nothing external | restart the container |
| `/readyz` (readiness) | should it receive traffic now? | DB/cache reachable, migrations done, warm-up finished, not shutting down | remove from load balancer |
Checking the database in liveness causes restart storms during a DB blip: every pod restarts and the outage gets worse.

## 2. Implementation
```js
let shuttingDown = false;
app.get("/livez", (req, res) => res.status(200).send("ok"));
app.get("/readyz", async (req, res) => {
  if (shuttingDown) return res.status(503).json({ status: "shutting_down" });
  try {
    await Promise.all([
      withTimeout(db.query("SELECT 1"), 500),
      withTimeout(redis.ping(), 300),
    ]);
    res.json({ status: "ready", version: process.env.GIT_SHA });
  } catch { res.status(503).json({ status: "unavailable" }); }
});
process.on("SIGTERM", () => {
  shuttingDown = true;                             // LB stops sending new requests
  setTimeout(() => server.close(() => process.exit(0)), 10_000);   // drain after probes notice
});
```
- Register health routes before auth, rate limiting and request logging (or exclude them) to avoid noise.
- Keep checks cheap and bounded; cache dependency status for a few seconds under heavy probe traffic.
- Do not include third-party APIs in readiness unless the service is useless without them.

## 3. Probe configuration (Kubernetes)
```yaml
livenessProbe:  { httpGet: { path: /livez, port: 3000 }, periodSeconds: 10, failureThreshold: 3 }
readinessProbe: { httpGet: { path: /readyz, port: 3000 }, periodSeconds: 5, failureThreshold: 2 }
startupProbe:   { httpGet: { path: /livez, port: 3000 }, periodSeconds: 5, failureThreshold: 30 }   # slow boots: 30 x 5 s = 150 s to start; liveness only takes over once it succeeds
```
Pair with a `preStop` sleep or the readiness flip so in-flight requests drain before exit.

## 4. Exposure
Return minimal JSON publicly (status, version). Detailed dependency diagnostics belong on an internal port or behind auth.

## Verify
- [ ] Killing the DB makes `/readyz` 503 while `/livez` stays 200; a rolling deploy shows zero 5xx at the load balancer.
