---
id: computing-software.cloud-infrastructure-engineering.aws.compute-optimizer-rds-and-aurora-rightsizing
name: compute-optimizer-rds-and-aurora-rightsizing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, compute-optimizer, rds-rightsizing, aurora, rds, idle-databases, graviton]
level: practitioner
status: docs-checked
description: "Rightsize RDS and Aurora with Compute Optimizer: enabling, reading instance and storage recommendations, idle findings, Graviton options, and validating before resizing."
sources: ["https://docs.aws.amazon.com/compute-optimizer/latest/ug/view-rds-recommendations.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_StopInstance.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute Optimizer RDS and Aurora rightsizing

## Enable and read
```bash
aws compute-optimizer update-enrollment-status --status Active --include-member-accounts
aws compute-optimizer get-rds-database-recommendations \
  --query 'rdsDBRecommendations[].{db:resourceArn,finding:instanceFinding,current:currentDBInstanceClass,options:instanceRecommendationOptions[0].dbInstanceClass,storage:storageFinding}'
```
(Fields come from the `RDSDBRecommendation` shape of the Compute Optimizer API.)
- Covers RDS for MySQL, RDS for PostgreSQL and Amazon Aurora databases.
- Findings (`instanceFinding`): **Optimized**, **Over-provisioned**, **Under-provisioned**; idle databases carry a separate `idle` flag.
- Instance class options with estimated savings and performance risk; storage recommendations (`storageFinding`).
- Compute Optimizer can recommend AWS Graviton-based instance classes; check the performance risk shown for each option.

## Validate before acting
- Look at CPU, memory (freeable memory, swap), connections, IOPS/throughput and buffer cache hit
  ratio in CloudWatch and Performance Insights over the lookback window, including month-end peaks.
- Memory-bound databases (large working sets) suffer when downsized even with low CPU; check freeable memory and read IOPS growth.
- Aurora: consider Serverless v2 for spiky workloads and I/O-Optimized vs Standard configuration based on I/O share of the bill.

## Resize safely
```bash
aws rds modify-db-instance --db-instance-identifier orders --db-instance-class <NEW_INSTANCE_CLASS> --apply-immediately
```
- Aurora: modify a reader, fail over to it, then modify the old writer.
- Check reserved instance coverage before changing instance family.

## Idle databases
Snapshot, tag with owner and date, stop (RDS starts a stopped instance again after 7 days) or delete after confirmation.

## Verify
- [ ] Recommendations reviewed monthly; changes tracked with before/after cost and performance.
- [ ] Post-resize: no rise in latency, swap, or read IOPS for two weeks.

## Checked

2026-10-28

Confirmed: supported engines (RDS MySQL, RDS PostgreSQL, Aurora), Graviton recommendations, estimated savings and performance risk (Compute Optimizer RDS page); RDSDBRecommendation fields instanceFinding, storageFinding, idle, currentDBInstanceClass, instanceRecommendationOptions[].dbInstanceClass (botocore); stopped instance restarts after 7 days (RDS User Guide); commands and flags (check_commands).

Removed: idle as a finding value (it is a separate flag), gp2 to gp3 example, db.r7g/db.m7g names, Multi-AZ interruption duration, reserved-instance size-flexibility claim, hedge about API name, FreeableMemory metric name.

Method: documentation only; no commands were run.
