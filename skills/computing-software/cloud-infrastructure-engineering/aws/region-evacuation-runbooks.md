---
id: computing-software.cloud-infrastructure-engineering.aws.region-evacuation-runbooks
name: region-evacuation-runbooks
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, multi-region, region-evacuation, route53-arc, regional-failover, disaster-recovery, runbooks]
level: practitioner
status: draft
description: "Write and rehearse a region evacuation runbook: decision criteria, data-plane-only traffic shift with ARC, data promotion, capacity, fencing the old region, and failback."
sources: ["Amazon Route 53 Application Recovery Controller Developer Guide - Routing control and Region switch", "AWS Whitepaper - Disaster Recovery of Workloads on AWS", "AWS Fault Isolation Boundaries whitepaper - control planes and data planes", "Amazon Aurora User Guide - Switchover and failover for Aurora Global Database"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Region evacuation runbooks

**Goal:** move a workload's traffic and writes out of an impaired region in minutes, using only
operations that do not depend on that region (or on global control planes) being healthy.

## Prerequisites (done before any incident)
- Target region has deployed stacks, quotas raised, and enough capacity (scaled warm standby or capacity reservations).
- Data replicated with known lag: Aurora Global Database, DynamoDB global tables, S3 CRR, ECR/AMI/secret/KMS multi-region copies.
- Traffic control on the **data plane**: Route 53 ARC routing controls or health-check-driven
  failover records, already created. Editing DNS records is a control-plane call (Route 53 control plane in us-east-1); flipping a routing control state is a data-plane call with regional endpoints.
- Credentials to operate from outside the impaired region (break-glass roles, IAM is global but STS regional endpoints in the healthy region).

## Runbook skeleton
1. **Decide:** criteria (e.g. error rate > X for 10 min with AWS Health issue in the region), who decides, max decision time.
2. **Freeze:** stop deployments and batch jobs in both regions.
3. **Fence writes in the impaired region:** flip routing so no clients write there; disable consumers if they can still run.
4. **Promote data:**
   `aws rds failover-global-cluster --global-cluster-identifier orders --target-db-cluster-identifier arn:...:cluster:orders-usw2 --allow-data-loss`
   (unplanned failover; use switchover without data loss for planned moves). DynamoDB global tables need no promotion.
5. **Shift traffic:** `aws route53-recovery-cluster update-routing-control-state --routing-control-arn ... --routing-control-state Off` using a cluster endpoint in a healthy region.
6. **Scale:** raise ASG/ECS desired counts, Lambda concurrency reservations.
7. **Verify:** synthetic checks, business KPIs, error rates in the target region.
8. **Communicate:** status page, stakeholders, record RPO actually lost.
9. **Failback later**, as a planned switchover after replication is re-established in the reverse direction.

ARC **Region switch** plans can orchestrate these steps (routing, Aurora, scaling, custom Lambda) as one executable plan; check current feature availability.

## Rehearse
Quarterly game day with FIS cross-region connectivity scenario or a planned switchover in production off-peak; measure time per step and fix the slowest.

## Gotchas
- Hidden single-region dependencies: SaaS webhooks pinned to one region's endpoint, hard-coded regional ARNs, S3 bucket names, CloudFront origins with no failover group.
- Async replication lag means data loss on unplanned failover: reconcile after the event.
- Client DNS caching extends the cut-over; Global Accelerator avoids DNS for faster shifts.

## Verify
- [ ] Runbook has owners, commands with real ARNs, and a timed last rehearsal under the RTO.
- [ ] Routing control state changes tested from a laptop with only healthy-region endpoints.
