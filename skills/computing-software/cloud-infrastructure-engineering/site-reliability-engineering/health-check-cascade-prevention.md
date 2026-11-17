---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.health-check-cascade-prevention
name: health-check-cascade-prevention
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [health-check-storms, health-check-failures-cascade, cascading-failures, liveness-probe, readiness-probe, fail-open]
level: advanced
status: docs-checked
description: "Stop health checks turning overload into outage: separate liveness, local and dependency checks, use fail-open load balancing, keep readiness independent of shared dependencies."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/", "https://aws.amazon.com/builders-library/implementing-health-checks/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Health check failures that cascade

A health check decides whether a server gets traffic or is restarted. If the check fails on many servers at
once for a shared reason, the fleet loses capacity exactly when it needs it. Kubernetes liveness probes
restart a container that fails; a failing readiness probe makes the EndpointSlice controller remove the Pod's
IP from matching Services.

## Patterns that cascade (illustrative)
- **Liveness probe that checks a shared dependency**: dependency slow -> every pod's liveness fails -> all
  pods restart together -> full outage and a reconnect burst.
- **Liveness timeouts too tight**: CPU saturated -> probe slow -> restart -> capacity drops.
- **Readiness removes too many**: overloaded pods marked unready -> fewer ready pods -> more overload.
- **Health checks queued behind work**: thread pool full -> health check waits -> fails.
- Restarting overloaded tasks makes things worse if the real problem is a cold cache (SRE Book, cascading
  failures: identify the cause before restarting, and canary the change).

## Check types (AWS Builders' Library, "Implementing health checks")
| Check | What it tests | Notes from the article |
|---|---|---|
| Liveness | basic connectivity and presence of the server process | often run by the load balancer; unaware of how the application works |
| Local health | resources not shared with peers (for example disk) | unlikely to fail on many servers at once |
| Dependency health | the server's dependencies | can fail fleet-wide, so be careful acting on them |

The article recommends the work producer (load balancer, queue poller) act on liveness and local checks, so
servers leave service automatically only for problems definitively local to that server, such as a bad disk.

## Fail open
When an individual server fails a health check the load balancer stops sending it traffic, but when all
servers fail at the same time a load balancer can fail open and allow traffic to all servers. That behaviour
is what makes it safer to include a dependency check. Check whether your own load balancer or proxy
implements fail-open (some call it a panic threshold) and its default, in that product's documentation.

## Kubernetes notes
- Liveness probes detect and remedy applications that have entered a broken state and cannot recover except by restart: keep them to that.
- Readiness removes a Pod from Service endpoints with no fail-open, so if every Pod is unready the Service has no
  ready endpoints. Keep readiness independent of shared dependencies.
- Serve health endpoints so they are not queued behind request work (for example a separate thread pool or listener).

## Verify
- [ ] Fault test: block the shared dependency; pods stay alive (not restarted) and serve errors or degraded responses.
- [ ] CPU stress test does not trigger liveness restarts.

## Checked
2026-11-01. Confirmed against the Kubernetes probe task page and pod lifecycle page (liveness restart, readiness
removal from EndpointSlices), the AWS Builders' Library article (liveness, local, dependency checks, fail open, who
should act on which) and the SRE Book cascading-failures chapter (restart caution). Removed: probe timing values,
Envoy `healthy_panic_threshold` and its default, the ALB fail-open claim, startup-probe formula and the
"health checks amplify overload" narrative as sourced fact (kept only as illustrative patterns).
Method: documentation only; no commands were run.
