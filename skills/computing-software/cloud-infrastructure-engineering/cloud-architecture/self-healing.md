---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.self-healing
name: self-healing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, reliability-foundations, self-healing, auto-recovery, health-probes, automatic-failover, self-preservation, remediation-automation]
level: practitioner
status: docs-checked
description: "Make workloads recover automatically (failure detection, failover, retries, automated actions) and survive failures with self-preservation, graceful degradation, fault injection."
sources: ["https://learn.microsoft.com/azure/well-architected/reliability/self-preservation", "https://learn.microsoft.com/azure/architecture/guide/design-principles/self-healing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-healing and self-preservation

Azure defines self-preservation as resilience against potential problems (it lowers the chance of
a full outage) and self-healing as automatically resolving issues by recovering affected
components and, if needed, failing over to redundant infrastructure (RE:07). The self-healing
design principle: detect failures, respond gracefully, and log and monitor failures.

## Self-healing mechanisms
- **Failure detection plus automatic response**: services expose a health endpoint covering their
  own state and their dependencies; load balancers, orchestrators and external monitors use it
  to route traffic.
- **Automated failover**: Virtual Machine Scale Sets and most PaaS compute, relational and
  NoSQL databases, and redundant storage can be configured for it. For stateless tiers, put
  multiple instances behind a load balancer or traffic manager; for stateful, use replicas
  (the application may need to handle eventual consistency).
- **Retry transient faults**, and use a circuit breaker so persistent failure does not overload a
  failing service and cascade.
- **Queue-based recovery**: a dead-letter queue stops a corrupt message blocking processing;
  moving messages there is automated, handling them usually needs manual evaluation.
- **Automated actions** triggered by monitoring on predetermined health changes, for example
  restarting an unresponsive app service; Azure Monitor action groups can trigger runbooks,
  functions, logic apps or webhooks.
- **Checkpoints** for long-running work so another instance can resume from durable state.

## Self-preservation
- Redundancy at different levels, avoiding single points of failure.
- Deployment stamps and bulkheads to minimise the blast radius.
- Loosely coupled components with asynchronous communication; avoid monolithic designs.
- Queue-based load levelling to buffer spikes; throttle clients that exceed quotas, and block
  consistently abusive ones with an out-of-band unblock process.
- Leader election so a coordinator is not a single point of failure.
- Graceful degradation as a distinct workflow: detect failed components, reroute automatically,
  tell users what changed, and keep essential flows alive (for example a read-only mode with
  cached data).

## Steps
1. Focus equally on local, short failures (lost connections) and rare large ones (regions).
2. Pick automated responses per critical flow from its reliability target.
3. Test the failure path with fault injection; chaos engineering extends this by introducing
   failures into production instances.
4. Log recovery so you can see failures and whether recovery worked.

## Gotchas
- The Azure page warns not to over-build: avoid self-healing in parts of the workload that do not
  need automated recovery, and keep it within cost, performance and downtime targets.
- Automating failover has a cost and can reduce performance compared with single-region.

## Verify
- [ ] Killing an instance recovers without human action within the target time.
- [ ] Degraded mode is tested and tells users what is unavailable.

## Checked
2026-11-08. Confirmed against the Azure Well-Architected self-healing and self-preservation page
(RE:07, definitions, automated failover list, checkpoints, automated actions, dead-letter queue,
graceful degradation, Azure Monitor action groups) and the Azure Architecture Center "Design for
self-healing" page (detect/respond/log, retries, health endpoints, circuit breaker, bulkhead,
load levelling, throttling, leader election, fault injection, chaos, do not over-build). Removed:
the numeric instance-replacement rate limits, the readiness-versus-liveness advice, the
EventBridge/SSM example and the AWS reliability pillar page (returned an empty page).
Method: documentation only; no commands were run.
