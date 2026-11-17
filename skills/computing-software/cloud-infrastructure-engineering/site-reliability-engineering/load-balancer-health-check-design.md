---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.load-balancer-health-check-design
name: load-balancer-health-check-design
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, load-balancing, lb-health-check-design, readiness-probes, liveness-probes, health-checks]
level: advanced
status: docs-checked
description: "Design load balancer and Kubernetes health checks: liveness, local and dependency checks, fail-open, startup probes, lame duck shutdown, avoiding fleet-wide cascades."
sources: ["https://aws.amazon.com/builders-library/implementing-health-checks/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/", "https://sre.google/sre-book/load-balancing-datacenter/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Load balancer health check design

**Goal:** remove genuinely broken instances quickly without ever removing the whole fleet because of a shared dependency.

## Types (AWS Builders' Library)
| Check | Answers | Notes |
|---|---|---|
| Liveness | Is the process present and accepting connections? | Port listening, basic HTTP 200, EC2 status checks; unaware of application details |
| Local health | Can this host serve? | Tests resources not shared with peers, so unlikely to fail fleet-wide: disk read/write, critical processes (proxy and app) running and answering correctly, support processes (monitoring daemons, metering, credential updates) present |
| Dependency (deep) | Are dependencies reachable? | Thorough but dangerous: a dependency problem can cascade through the whole fleet |

Core tension: thorough checks and quick mitigation of single-server failures against the harm of a false positive
across the entire fleet. Automation should stop directing traffic to one bad server but keep allowing traffic if
the whole fleet appears to be having trouble.

## Rules
- Configure the work producer (load balancer, queue polling thread) to run liveness and local checks, so servers
  are removed automatically only for problems definitively local to that server, such as a bad disk. Run
  dependency checks and anomaly detection from other external monitoring systems, which can alarm, engage an
  operator or terminate instances.
- **Fail open**: when one server fails a check the load balancer stops sending it traffic, but when all servers
  fail at once a load balancer that fails open sends traffic to all of them. Know your load balancer's behaviour.
- Even one API can behave differently by input: a read API that caches responses can keep serving when the
  database is down, so failing the health check for one unhealthy code path widens the impact.
- Fleet automation needs rate limiting, thresholds and circuit breakers that hand over to humans in uncertain or
  extreme situations.
- Services with shallow checks can leave a bad queue worker (disk full, out of file descriptors) pulling work
  quickly and failing it, so queue consumers need deeper local checks too.

## Kubernetes probes
- A **startup probe** protects slow-starting containers: use the same check as the liveness probe with
  `failureThreshold * periodSeconds` long enough for the worst-case startup. After it succeeds once the
  liveness probe takes over; if it never succeeds the container is killed and subject to `restartPolicy`.
- A **readiness probe** covers an app temporarily unable to serve (loading large data, depending on external
  services): the pod is not killed but receives no traffic through Services. Readiness probes run for the whole
  container lifecycle, and readiness and liveness probes do not depend on each other.
```yaml
livenessProbe:  { httpGet: { path: /healthz, port: 8080 }, failureThreshold: 1, periodSeconds: 10 }
startupProbe:   { httpGet: { path: /healthz, port: 8080 }, failureThreshold: 30, periodSeconds: 10 }  # 5 min max startup
```
- Detection time is roughly interval times failure threshold; tune the numbers for your service.

## Lame duck shutdown (SRE Book, Load Balancing in the Datacenter)
A backend task can enter a lame duck state: it tells clients to send new requests elsewhere (in Google's RPC
implementation via an API call in the SIGTERM handler), finishes requests already started, then exits. This avoids
serving errors to requests active on a task that is shutting down, and simplifies pushes and maintenance.

## Verify
- [ ] Chaos test: stop the database; instances stay in rotation rather than all being removed; kill one instance's process and it leaves rotation.

## Checked

Checked 2026-11-09. Confirmed against the AWS Builders' Library page on implementing health checks, the Kubernetes probe task page (startup and readiness semantics, the 30 x 10 second example) and the SRE Book Load Balancing in the Datacenter page (lame duck state). Removed: the Envoy panic threshold and ALB/ELB claims, the specific readiness and liveness interval numbers, the statements about overload hysteresis, separate thread pools and unauthenticated endpoints, none of which appeared on a page read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
