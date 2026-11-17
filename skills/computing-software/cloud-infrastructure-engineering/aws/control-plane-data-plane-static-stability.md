---
id: computing-software.cloud-infrastructure-engineering.aws.control-plane-data-plane-static-stability
name: control-plane-data-plane-static-stability
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, control-plane-dependency, data-plane, static-stability, well-architected-reliability, availability-zone-independence, recovery-design, us-east-1-dependency, pre-provisioned-capacity, failover-design, dependency-analysis]
level: sme
status: docs-checked
description: "Design recovery that avoids impaired control planes: classify control vs data plane APIs in a failover path, pre-provision capacity and credentials, test static stability."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/control-planes-and-data-planes.html", "https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/static-stability.html", "https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/global-services.html", "https://aws.amazon.com/builders-library/static-stability-using-availability-zones/", "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_withstand_component_failures_static_stability.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control plane vs data plane dependencies (static stability)

**Goal:** the steps you take to survive an AZ or Region impairment use only **data plane**
operations that were already set up, because control planes (create/modify/delete APIs)
are more complex, less available and often the first thing degraded in an event.

## 1. The distinction
- **Control plane**: administrative APIs that create, change or delete resources —
  `RunInstances`, creating DB instances, Route 53 record changes, IAM
  role creation, ASG scaling that launches instances, ECS service updates that place tasks.
- **Data plane**: the running resource doing its job — an instance serving traffic, DNS
  answering queries, Route 53 health checks evaluating, STS issuing credentials for an
  existing role, an existing ALB routing, a DynamoDB read.
- Data planes are designed to keep working when their control plane is impaired.

## 2. Audit a recovery runbook
For each step write: API called → control or data plane → which Region/partition hosts
it → what you do if it fails.
| Typical step | Plane | Statically stable alternative |
|---|---|---|
| Launch instances in the surviving AZ/Region when needed | Control (EC2) | Pre-provision N+1 capacity across AZs; warm standby already running |
| Edit DNS records to point at DR | Control (Route 53, homed in us-east-1) | Pre-created failover records + health checks or ARC routing controls (data plane) |
| Create IAM roles/users for responders | Control (IAM, us-east-1) | Roles exist in advance; break-glass credentials stored |
| Promote a read replica / fail over Aurora Global | Control in the healthy Region | Acceptable: healthy Region's control plane; rehearse it |
| Scale ECS/ASG up in DR | Control in the healthy Region | Acceptable if capacity is likely; reserve capacity for critical tiers |

## 3. Patterns
- **AZ static stability**: run enough capacity in each AZ that losing one leaves enough to
  carry peak (with 3 AZs, overprovision by 50 percent so each AZ runs at about 66 percent of its tested capacity), rather than relying on ASG to relaunch.
- **Cell/zonal independence**: keep traffic AZ-local (ALB cross-zone off where sensible,
  zonal endpoints) so one AZ's failure stays local; use **zonal shift/autoshift** (ARC) to
  move away from an AZ — a data-plane-style action.
- **Global service awareness**: IAM, Organizations, Route 53 control planes, CloudFront
  config, and some others are homed in us-east-1 for the aws partition. Avoid them in
  recovery paths.
- **Credentials**: use Regional STS endpoints (`AWS_STS_REGIONAL_ENDPOINTS=regional`) so
  credential issuance does not depend on the global endpoint.
- **Configuration at runtime**: cache config and secrets locally with sensible TTL so a
  Parameter Store/Secrets Manager blip does not stop running services.

## 4. Test it
- Game days with **FIS**: network disruption to one AZ and zonal-autoshift actions.
- Simulate "no control plane": during a drill, deny control-plane actions (instance launch, DNS changes, IAM writes)
  via an SCP on the test account and execute the runbook. Anything that fails
  is a control-plane dependency.

## Gotchas
- Autoscaling feels like resilience but is a control-plane dependency at the worst
  moment; capacity may also be scarce in the surviving AZs during an event.
- Health checks that fail open (or closed) on dependency errors can trigger mass failover;
  separate liveness from deep health.
- Infrastructure-as-code pipelines are control-plane heavy; do not plan to "redeploy" as
  the recovery.

## Verify
- [ ] Runbook table lists plane and Region for every step; no us-east-1 control-plane call in the failover path (unless that is the healthy Region).
- [ ] SCP-deny drill passes: failover completes with control-plane writes denied.
- [ ] Per-AZ capacity covers peak with one AZ removed (load test or FIS AZ experiment).

## Checked

2026-10-28

Confirmed: IAM, Organizations, Route 53 public DNS and CloudFront control planes in us-east-1 (fault isolation boundaries whitepaper); AZ overprovisioning example of 50 percent for three AZs (Builders' Library static stability); AWS_STS_REGIONAL_ENDPOINTS (SDK reference guide); zonal autoshift in ARC (FIS actions reference); RunInstances idempotency token (Builders' Library).

Removed: Identity Center row, ODCR term, CreateDBInstance/ChangeResourceRecordSets/CreateRole/GetItem names, SCP action names, FIS scenario name; corrected the '3 AZs at 50% each' example to the Builders' Library figure.

Method: documentation only; no commands were run.
