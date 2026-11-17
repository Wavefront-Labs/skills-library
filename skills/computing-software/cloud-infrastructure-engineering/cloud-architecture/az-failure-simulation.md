---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.az-failure-simulation
name: az-failure-simulation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resilience-testing, az-failure-simulation, availability-zone-outage, fis-az-power-interruption, zone-down-test, chaos-studio-zone]
level: advanced
status: docs-checked
description: "Simulate an availability-zone failure safely: scenario choice (power interruption, network blackhole), scope, capacity checks, data-tier behaviour, observation and recovery."
sources: ["https://docs.aws.amazon.com/fis/latest/userguide/az-availability-scenario.html", "https://learn.microsoft.com/azure/chaos-studio/chaos-studio-fault-library", "https://learn.microsoft.com/azure/reliability/availability-zones-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Availability-zone failure simulation

## Scenarios
- **AWS FIS "AZ Availability: Power Interruption"** scenario: stops EC2 instances (including
  EKS/ECS-managed and Auto Scaling) in one AZ with `aws:ec2:stop-instances`, makes instance
  launches fail in that AZ, blocks subnet connectivity for 2 minutes with
  `aws:network:disrupt-connectivity`, fails over RDS multi-AZ clusters
  (`aws:rds:failover-db-cluster`), interrupts ElastiCache replication groups, leaves one EBS volume
  unresponsive (`aws:ebs:pause-io`). Default: 30 minutes of power-interruption symptoms plus 30
  minutes of recovery symptoms. Targets are chosen by tags such as `AzImpairmentPower`; actions
  with no targets are skipped. The scenario has no stop conditions: add your own.
- **Azure Chaos Studio**: Virtual Machine Scale Set Shutdown version 2.0 with a zone filter (an
  experiment fails if the filter matches no targets), the NSG Security Rule fault, and AKS Chaos
  Mesh faults. Azure manages zone-redundant resources and their failover, so you cannot select a
  zone to fail for them; zonal resources need you to run failover yourself.

## Steps
1. Hypothesis with your own numbers: "With zone A lost at peak-like load, error rate stays below
   X% and p99 below Y ms; the DB fails over within Z seconds."
2. Pre-checks: other zones' capacity and quotas, alarms in place, stop conditions, comms to stakeholders.
3. Start in staging with production-like topology; then production in a low-traffic window.
4. Observe: per-AZ metrics, LB target health, DB failover time, queue backlogs, client errors.
5. Recover: end experiment, confirm instances restart and capacity rejoins.
6. Write findings: hidden zonal dependencies (for example single-AZ RDS nodes, which AWS
   documents as fully unavailable in the scenario).

## Gotchas
- Simulating with only instance termination misses the network and dependency behaviour.
- Single-AZ RDS nodes are fully unavailable; only multi-AZ clusters fail over.

## Verify
- [ ] Hypothesis met or gaps ticketed; repeat after fixes.

## Checked
2026-11-08. Confirmed: AWS FIS AZ Availability: Power Interruption page (actions and fault names, 30+30 minute default, 2-minute connectivity block, tag-based targets, skipped actions, no stop conditions, single-AZ RDS unavailable) and Azure Chaos Studio fault library (VMSS Shutdown 2.0 zone filter and failure on empty filter, NSG Security Rule, AKS Chaos Mesh) and Azure availability zones overview (Microsoft manages zone-redundant failover; zonal failover is the customer's job). Removed: NACL swap, specific latency/error thresholds (now placeholders), rebalancing claims, NAT gateway example.
Method: documentation only; no commands were run.
