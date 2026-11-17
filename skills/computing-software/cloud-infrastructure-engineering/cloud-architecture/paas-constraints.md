---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.paas-constraints
name: paas-constraints
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, service-models, paas-constraints, paas, app-service, cloud-run, elastic-beanstalk, platform-limits, escape-hatch]
level: practitioner
status: docs-checked
description: "Check a PaaS against the workload before committing: request timeouts, filesystem, sockets, scaling limits, runtime versions, networking and the exit path when you outgrow it."
sources: ["https://learn.microsoft.com/azure/app-service/overview", "https://cloud.google.com/run/quotas", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.html", "https://csrc.nist.gov/pubs/sp/800/145/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PaaS platform constraints and escape hatches

PaaS buys you patching, scaling and deployment plumbing by taking away control. The failures come
from constraints nobody read before the first production incident.

## Constraint checklist (verify each against current docs for the chosen platform)
| Area | Question | Typical limits seen |
|---|---|---|
| Request duration | Max request / response time? | Cloud Run services: request timeout maximum 60 minutes (quotas page); check the front end and any gateway in front |
| Filesystem | Writable? Persistent? Shared across instances? | Look up per platform |
| Inbound protocols | HTTP/1.1 only, HTTP/2, gRPC, WebSockets, raw TCP/UDP? | Raw TCP/UDP rarely allowed |
| Outbound | Static egress IP? Outbound connection limits? | Look up per platform |
| Background work | CPU when no request is in flight? | Cloud Run guarantees CPU only while at least one request is being processed (container contract); check the CPU allocation setting |
| Scaling | Max instances, cold start, concurrency per instance | Cloud Run quotas list a maximum number of instances per project and region (adjustable); concurrency defaults differ per platform |
| Runtime | Supported language versions and EOL cadence | Platform retires old runtimes on its schedule, not yours |
| Networking | Private ingress, VNet/VPC integration, private endpoints to data stores | Look up per platform and tier |
| Observability | Log shipping, custom metrics, tracing agent support | Sidecars may not be allowed |
| Compliance | Region availability, isolation tier (dedicated or isolated options) | Look up per platform |

## Procedure
1. List the workload's needs from NFRs (latency, request length, protocols, state, compliance).
2. Map each to the platform limit table; mark hard blockers vs workarounds.
3. Spike the riskiest constraint (long request, WebSockets, egress volume) on the real platform.
4. Record the **escape hatch**: package as an OCI container and keep config in env vars
   (twelve-factor), so moving to a container platform or Kubernetes is a redeploy, not a rewrite.
5. Write the decision as an ADR including the limits accepted.

## Gotchas
- Buildpack-based platforms pin you to their build; prefer container images you build yourself.
- Platform-specific SDKs (proprietary queues/config bindings) are the real lock-in, not the runtime.
- Autoscaling is still bounded by instance quotas (Cloud Run lists a per-project, per-region maximum); request increases ahead of launches.
- Outbound connection exhaustion looks like random timeouts; fix with connection pooling.

## Checked
2026-10-28. Confirmed: Cloud Run quotas (60 minute request timeout for services, maximum instances per project and region, adjustable), Cloud Run container contract (CPU allocated while a request is processed), and the NIST SP 800-145 and PaaS overview pages for the model itself. Removed: App Service 230 s, SNAT ~128 ports, `/home`, API gateway 29-30 s, Cloud Run concurrency default of 80, the "premium tier" and isolation-cost remarks (not confirmed in the fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Every NFR mapped to a limit with evidence (doc link or spike result).
- [ ] Container image runs locally and on one alternative platform.
- [ ] ADR records accepted constraints and exit path.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.service-model-selection
