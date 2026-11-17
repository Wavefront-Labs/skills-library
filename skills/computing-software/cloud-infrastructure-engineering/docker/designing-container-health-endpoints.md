---
id: computing-software.cloud-infrastructure-engineering.docker.designing-container-health-endpoints
name: designing-container-health-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, healthcheck, health-endpoint-design, readiness-check, liveness, container-health, kubernetes-probes]
level: advanced
status: docs-checked
description: "Design what a container health check tests: shallow liveness vs dependency-aware readiness, avoiding cascading restarts, timeouts and cost, and mapping to Docker and Kubernetes."
sources: ["https://docs.docker.com/reference/dockerfile/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Designing container health endpoints

Docker has one health concept; Kubernetes has three (startup, liveness, readiness). Design
endpoints so the same image works under Docker, Compose, Swarm and Kubernetes.

## Two endpoints
| Endpoint | Answers | Checks | Failure action |
|---|---|---|---|
| `/livez` (liveness) | Is this process wedged? | Event loop responsive, no deadlock; **no** external calls | Restart the container |
| `/readyz` (readiness) | Can this instance serve traffic now? | Own warmup done, critical deps reachable (DB pool, required cache) | Stop routing traffic, do not restart |

Docker's `HEALTHCHECK` tests that a container is still working, for example a web server stuck in
an infinite loop that cannot handle new connections. Keep the Docker check shallow (liveness-style)
and let the orchestrator's readiness probe carry dependency checks.

## Rules
- Never restart on dependency failure: if the DB is down and every API container's health
  check fails, an orchestrator that restarts on failed checks restarts them all, adding a
  thundering herd on recovery.
- Fast and cheap, no auth. The check runs every `interval` in every replica forever.
- Timeouts inside the handler shorter than the check timeout, so the endpoint returns a
  clear 503 instead of the checker killing it.
- Return machine-readable detail for humans, but decide on status code only:
```json
{ "status": "fail", "checks": { "db": "timeout after 500ms", "cache": "ok" } }
```
- Exempt health paths from rate limiting, access logs (or sample them) and tracing.

## Checker inside the image
Prefer a tiny binary or the app itself over shell + curl:
```dockerfile
HEALTHCHECK --interval=15s --timeout=3s --start-period=30s --retries=3 \
  CMD ["/app/server", "healthcheck", "--url=http://127.0.0.1:8080/livez"]
```
Worker containers with no HTTP: touch a heartbeat file each loop and check its age:
```dockerfile
HEALTHCHECK CMD ["sh", "-c", "test $(( $(date +%s) - $(stat -c %Y /tmp/heartbeat) )) -lt 60"]
```

## Mapping to Kubernetes
Define Kubernetes probes in the pod spec rather than relying on the image's `HEALTHCHECK`. Map
`/livez` to `livenessProbe` (a failing liveness probe makes the kubelet kill and restart the
container), `/readyz` to `readinessProbe`, and `start-period` to a `startupProbe`.

## Verify
```bash
docker inspect <c>     # the State.Health section shows status and recent check results
```

## Checked
Checked 2026-10-28 against the Dockerfile reference (`HEALTHCHECK` forms, `--interval` and
`--timeout` default 30s, `--start-period` default 0s, `--retries` default 3, only the last
`HEALTHCHECK` counts, `HEALTHCHECK NONE`) and the Kubernetes probes task page (liveness failure
leads to container restart). Removed as unconfirmed: Swarm and autoheal restart behaviour,
Compose `service_healthy` and `up --wait`, the 100 ms budget, the claim that Kubernetes ignores
`HEALTHCHECK`, the `failureThreshold` formula, the .NET health-check source and the exact
`State.Health.Log` template. The `/livez` and `/readyz` names are a convention, not a requirement.
Method: documentation only; no commands were run.
