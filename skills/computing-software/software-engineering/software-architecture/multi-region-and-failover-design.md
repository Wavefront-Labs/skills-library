---
id: computing-software.software-engineering.software-architecture.multi-region-and-failover-design
name: multi-region-and-failover-design
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, resilience, multi-region, failover, disaster-recovery, active-active, rto-rpo]
level: advanced
status: draft
description: "Design multi-region deployments: active-passive vs active-active, data replication and RPO, traffic failover, regional isolation, and rehearsed failover runbooks."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html", "https://cloud.google.com/architecture/dr-scenarios-planning-guide", "https://learn.microsoft.com/en-us/azure/well-architected/reliability/disaster-recovery"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-region and failover design

## Start from RTO/RPO and cost
| Pattern | RTO | RPO | Cost |
|---|---|---|---|
| Backup and restore to another region | hours | hours | low |
| Pilot light (data replicated, minimal compute) | tens of minutes | minutes | low-medium |
| Warm standby (scaled-down full stack) | minutes | seconds-minutes | medium |
| Active-active | ~0 (traffic shift) | ~0 to seconds | high, complex |
Multi-AZ in one region handles most failures; go multi-region for regional outages, data
residency, or latency to global users.

## Data is the hard part
- Async replication (most databases, S3 CRR) = non-zero RPO; writes in flight at failover are lost
  or must be reconciled.
- Active-active writes need conflict handling: partition ownership by key (each user homed in one
  region), CRDTs/last-writer-wins where acceptable, or a globally consistent database (Spanner,
  CockroachDB, DynamoDB global tables with LWW, Aurora Global Database for single-writer).
- Avoid cross-region synchronous calls in the request path.

## Traffic
DNS failover (Route 53 health checks, low TTL; clients cache longer than TTL), anycast/global load
balancers (Cloudflare, GCP global LB, AWS Global Accelerator). Decide automatic vs human-triggered
failover; automatic failover on flaky health checks causes flapping and split brain.

## Regional independence
Each region must run without the other: no shared control-plane dependency (single-region IAM,
secrets, CI, DNS provider), static stability (pre-scaled capacity in standby, no need to call
APIs to scale during the disaster).

## Runbook and rehearsal
Documented, scripted failover and **failback**, run quarterly as a game day with real traffic.
Measure actual RTO/RPO against targets. An untested DR plan is a hypothesis.
