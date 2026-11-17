---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.control-plane-data-plane
name: control-plane-data-plane
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, fault-isolation, control-plane-data-plane, static-stability, control-plane-dependency, data-plane-availability, recovery-design]
level: advanced
status: draft
description: "Separate control plane and data plane in your designs and dependencies: keep serving when control planes fail, avoid control-plane calls in recovery paths, cache config locally."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/control-planes-and-data-planes.html", "https://aws.amazon.com/builders-library/avoiding-overload-in-distributed-systems-by-putting-the-smaller-service-in-control/", "https://learn.microsoft.com/azure/reliability/concept-redundancy-replication-backup"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Control plane vs data plane separation

## Definitions
- **Control plane**: create/update/delete and configure (launch instances, change DNS records,
  update IAM, scale clusters). More complex, lower availability targets.
- **Data plane**: serving the actual function (instances running, DNS answering, IAM evaluating,
  storage read/write). Simpler, higher availability.

## Design rules
1. **Recovery must not depend on control planes**: failover by data-plane mechanisms (health
   checks that move traffic, pre-provisioned standby) instead of "create resources during the
   outage". AWS recommends e.g. Route 53 health-check failover (data plane) over editing records
   (control plane) in emergencies; ARC routing controls are data-plane switches.
2. **Static stability**: pre-provision capacity so a zone/region loss needs no scaling API calls.
3. **Cache configuration** locally (last-known-good) so a config service outage doesn't stop serving.
4. **Global services**: many global control planes (e.g. IAM, Route 53, CloudFront config) are
   hosted in one region; data planes are global. Do not put their control-plane calls in recovery.
5. In your own systems, build the same split: the serving path must not call the admin API.

## Gotchas
- Runbooks whose first step is "launch new instances in region B" during a provider-wide
  control-plane event.
- Kubernetes: workloads keep running if the API server is down, but autoscaling and rescheduling
  stop; plan headroom.

## Verify
- [ ] DR runbook reviewed: every step classified control vs data plane.
- [ ] Simulated config service outage: data path continues serving.
