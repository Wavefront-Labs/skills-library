---
id: computing-software.devops-ci-cd.deployment-strategies.capacity-and-cost-of-blue-green-fleets
name: capacity-and-cost-of-blue-green-fleets
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, double-capacity, blue-green, capacity-planning, deployment-cost, warm-standby, quota-limits]
level: practitioner
status: draft
description: "Plan capacity and cost for blue-green deployments: doubling compute during cutover, quotas and IP space, keeping green warm, shrinking idle blue, and cheaper hybrids."
sources:
  - https://docs.aws.amazon.com/whitepapers/latest/blue-green-deployments/welcome.html
  - https://martinfowler.com/bliki/BlueGreenDeployment.html
  - https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-groups-create-blue-green.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Capacity and cost of doubled fleets

Blue-green needs two full production environments at the moment of switch. That doubles peak spend and stresses limits that never matter in rolling updates.

## What actually doubles
- Compute (instances, pods, tasks) for the duration green is up before blue is torn down.
- Things provisioned per environment: load balancers/target groups, NAT/egress, licences per host, monitoring agents billed per host.
- **Not** usually doubled: shared databases, caches, queues - which is also why schema changes must be backward compatible with both colours.

## Limits to check before the first switch
| Limit | Example |
|---|---|
| cloud quotas | EC2 vCPU on-demand quota per family, Fargate task quota, regional public IPs |
| subnet IP space | a /24 with 200 pods per colour can't hold 400 |
| cluster capacity | Kubernetes nodes and autoscaler max size must allow 2x replicas |
| connection limits | DB `max_connections` when both fleets open pools during overlap |
| licences | per-core/per-host software running in both colours |
| spot/AZ capacity | can the region actually give you 2x of that instance type right now? |
Run a capacity check job before deploying (`aws service-quotas get-service-quota`, cluster autoscaler max, free IPs per subnet) and fail early.

## Reducing the cost
- Keep the overlap short: create green just in time, switch, keep blue only for the rollback window (e.g. 1-24 h), then scale blue to zero.
- Scale-down-but-keep: blue at minimal replicas with autoscaling armed; rollback means switching traffic and letting it scale (slower rollback, much cheaper).
- Use blue-green only for the tier that needs instant rollback (stateless front ends), rolling or canary for others.
- Canary with automated analysis often gives the same safety with ~10-20% extra capacity instead of 100%.
- Kubernetes: Argo Rollouts blue-green with `scaleDownDelaySeconds` and `previewReplicaCount` (smaller preview fleet, scale to full before promotion).
- Reserved/committed spend sized for 1x; the 2x peak runs on on-demand or spot for short periods.

## Warm-up
Green at full size but cold (JIT, caches, connection pools) can fail at switch. Pre-warm with synthetic traffic or a short weighted shift (10% then 100%) and watch latency.

## Verify
- [ ] Capacity pre-check passes for 2x the current fleet (quota, IPs, nodes, DB connections).
- [ ] Blue is scaled down or deleted automatically after the rollback window; cost dashboard shows short spikes only.
