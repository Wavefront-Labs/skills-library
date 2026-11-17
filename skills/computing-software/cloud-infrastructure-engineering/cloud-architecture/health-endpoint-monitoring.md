---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.health-endpoint-monitoring
name: health-endpoint-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resiliency-patterns, health-endpoint-monitoring, health-checks, liveness-probe, readiness-probe, startup-probe, load-balancer-health-check, synthetic-monitoring, deep-health-check]
level: practitioner
status: docs-checked
description: "Design health endpoints that help: liveness vs local vs dependency checks, which consumer (LB, orchestrator, monitor) calls which, fail-open and avoiding fleet-wide ejection."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/health-endpoint-monitoring", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/", "https://aws.amazon.com/builders-library/implementing-health-checks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Health endpoint monitoring

Expose endpoints that external tools call at intervals; the monitor evaluates status code, content and latency. Use separate endpoints when consumers need different signals: a responsive process is not necessarily ready, and restarting it does not fix a failed shared dependency.

## Depth of check
| Check | Tests | Typical consumer |
|---|---|---|
| Liveness (shallow) | Process present and answering (listening port, basic HTTP 200). No downstream calls. | Orchestrator or LB; shallow so a dependency outage does not trigger restarts |
| Local health | Resources not shared with peers: disk read/write, critical processes answering correctly, support processes present. Unlikely to fail on many servers at once. | LB or queue poller (AWS Builders' Library) |
| Dependency / deep | Application plus required dependencies (database, cache, downstreams). | Readiness where a dependency failure makes the instance useless (Azure); external monitor and alarms (AWS) |

Azure advises excluding optional dependencies from the decision to remove an instance. AWS is more cautious: dependency checks can produce correlated false positives (a shared-dependency outage fails every server), so Amazon teams restrict fast-acting load balancer checks to liveness and local checks and leave dependency checks to monitoring systems with thresholding, rate limits and humans in the loop. Decide per service which stance fits; if you check dependencies in the LB path, design for the failure below.

## Fleet-wide ejection and fail open
If every server fails a dependency check at once, naive automation removes the whole fleet. Per AWS, Network Load Balancer fails open when no targets are healthy (and fails out of an Availability Zone whose servers are all unhealthy), and Application Load Balancer and Route 53 also support fail open. Test partial dependency failures too: a slow or lightly erroring data store can make servers flap without reaching the fail-open threshold. Azure also warns that a deep probe on a slow dependency can cascade; mitigate with per-dependency timeouts, circuit breakers or reporting degraded rather than unhealthy for non-critical dependencies. In Azure App Service, if all instances are unhealthy it does not exclude all of them.

## Probe settings
- Kubernetes: HTTP probes succeed on codes from 200 up to but excluding 400. A `startupProbe` protects slow starters: allowed startup time is `failureThreshold * periodSeconds` (30 x 10 = 5 minutes in the docs example), after which liveness takes over; if it never succeeds the container is killed and subject to `restartPolicy`. Liveness and readiness probes do not wait on each other; use `initialDelaySeconds` or a startup probe to delay. A failing readiness probe marks the pod unready so Services stop sending it traffic.
- Set timeouts and failure thresholds so transient faults do not trigger action. Allow for initialisation.
- Keep checks cheap: heavy deep checks consume connections and CPU and can exceed monitor timeouts. Caching the status adds a staleness window sized by its TTL.
- Overloaded servers should prioritise health checks (AWS): reserve spare workers so probes get connections, or a brownout can spiral as slow servers are ejected.

## Security
Restrict endpoints: require authentication the monitor supports, restrict network sources, return minimum information on the public path and require authorisation for detailed diagnostics. An obscure path or port is not access control.

## External monitoring
Run checks from locations representing users and validate agent correctness (for example, an endpoint returning a known value). Combine probes with metrics, logs and traces in a workload health model; alert on health of critical flows rather than single probe failures. Failover needs redundant capacity across the failure boundary, sized to absorb rerouted traffic.

## Gotchas
- A 200 only proves protocol-level availability; decide whether response content is validated.
- Synthetic transactions that change state need isolated test data.

## Verify
- [ ] Disable a dependency in staging: confirm what each consumer (LB, orchestrator, monitor) does and that the fleet is not wholly ejected.
- [ ] Slow-start instance is not killed during boot.

## Checked
2026-11-08, documentation only.
Confirmed against: Azure Architecture Center, Health Endpoint Monitoring pattern (last updated 2026-09-26); Kubernetes, Configure Liveness, Readiness and Startup Probes; AWS Builders' Library, Implementing health checks.
Removed as unconfirmed: the `/livez`, `/readyz` and `/health/deep` names, example LB interval and threshold figures, shutdown deregistration ordering, the "200 with body unhealthy" claim and restart-loop-during-maintenance example.
Method: documentation only; no commands were run.
