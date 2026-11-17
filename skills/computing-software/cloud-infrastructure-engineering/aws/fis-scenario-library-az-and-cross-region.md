---
id: computing-software.cloud-infrastructure-engineering.aws.fis-scenario-library-az-and-cross-region
name: fis-scenario-library-az-and-cross-region
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, fault-injection-service, fis, scenario-library, cross-region-connectivity, az-power-interruption, chaos-engineering]
level: practitioner
status: gated
description: "FIS scenario library: AZ Availability Power Interruption and Cross-Region Connectivity scenarios, targeting by tags, required roles and stop conditions, and safe first runs."
sources: ["https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FIS scenario library: AZ and cross-region scenarios

**What scenarios are:** pre-built experiment templates combining many actions to emulate a real
event. You pick a scenario, set targets (usually tags) and parameters, and FIS creates the template.

## AZ Availability: Power Interruption
Emulates losing one AZ's power (gated: unconfirmed, source is paywalled or blocked). Actions available in FIS (actions reference):
- `aws:ec2:stop-instances`, `aws:ebs:pause-volume-io`,
- EC2 API insufficient-capacity-error actions,
- `aws:network:disrupt-connectivity` on subnets in the AZ.
Targets come from tags you apply, so you control exactly what is affected.

## Cross-Region: Connectivity
Emulates loss of connectivity from a region to others (gated: unconfirmed, source is paywalled or blocked):
- `aws:network:route-table-disrupt-cross-region-connectivity` and `aws:network:transit-gateway-disrupt-cross-region-connectivity`,
- `aws:dynamodb:global-table-pause-replication`,
Tests whether the secondary region stands alone and whether the primary degrades gracefully.

## Prerequisites
- Experiment role with permissions for every action (the actions reference lists the AWS managed policy per action, for example `AWSFaultInjectionSimulatorEC2Access` and `AWSFaultInjectionSimulatorNetworkAccess`).
- **Stop conditions:** CloudWatch alarms on customer-facing SLOs; FIS stops when any is in ALARM. (gated: unconfirmed, source is paywalled or blocked)
- Logging to CloudWatch Logs/S3 and an experiment report configuration.
- Multi-account experiments if the workload spans accounts.

## First runs
1. Staging, with a narrow tag set and short duration (10 minutes).
2. Watch dashboards; confirm recovery actions (ASG rebalancing into other AZs, DB failover time).
3. Fix findings (missing multi-AZ, hard-coded AZ, slow health checks), rerun.
4. Production during business hours with the team watching, announced in advance, stop conditions armed.

## Gotchas
- Scenario templates are snapshots: update tags and parameters as architecture changes.
- Disrupting connectivity also cuts your access paths (bastions, SSM) in that AZ.
- Some managed services cannot be impaired by FIS; the scenario documents what is and is not covered.

## Verify
- [ ] Experiment completes with stop conditions armed; SLOs held or findings recorded.
- [ ] Hypothesis written before the run and compared with the report after.

## Checked

2026-10-28

Confirmed: action names aws:ec2:stop-instances, aws:ebs:pause-volume-io, aws:network:disrupt-connectivity, route-table and transit-gateway cross-region disruption, aws:dynamodb:global-table-pause-replication, AWSFaultInjectionSimulatorEC2Access and NetworkAccess managed policies, zonal autoshift action (FIS actions reference).

Removed: scenario composition details (RDS, ElastiCache, ECS/EKS, recovery step), tag examples, S3 replication pause, trust-principal claim, RDSAccess policy name; replaced prose sources.

Gated: the scenario descriptions (power interruption and cross-region connectivity as packaged scenarios) and the stop-condition behaviour: the Scenario library and Stop conditions pages returned empty pages.

Method: documentation only; no commands were run.
