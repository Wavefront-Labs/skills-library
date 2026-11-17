---
id: computing-software.cloud-infrastructure-engineering.aws.aurora-replica-auto-scaling
name: aurora-replica-auto-scaling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aurora, aurora-replica-auto-scaling, application-auto-scaling, reader-endpoint, read-scaling, promotion-tier]
level: practitioner
status: docs-checked
description: "Scale Aurora read capacity automatically with Application Auto Scaling target tracking on reader CPU or connections, cooldowns, promotion tiers and reader endpoint behaviour."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Integrating.AutoScaling.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Integrating.AutoScaling.Add.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aurora replica auto scaling

## 1. What it does
Application Auto Scaling adds or removes **Aurora Replicas** (readers) in a provisioned
cluster to keep a metric at a target: average reader CPU (`RDSReaderAverageCPUUtilization`)
or average connections (`RDSReaderAverageDatabaseConnections`), or a custom metric.
Auto-scaled replicas use the same instance class as the cluster's primary (writer)
instance.

## 2. Configure
```bash
aws application-autoscaling register-scalable-target --service-namespace rds \
  --resource-id cluster:orders-aurora --scalable-dimension rds:cluster:ReadReplicaCount \
  --min-capacity 1 --max-capacity 8
aws application-autoscaling put-scaling-policy --service-namespace rds \
  --resource-id cluster:orders-aurora --scalable-dimension rds:cluster:ReadReplicaCount \
  --policy-name reader-cpu-60 --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration '{
    "TargetValue": 60.0,
    "PredefinedMetricSpecification": {"PredefinedMetricType": "RDSReaderAverageCPUUtilization"},
    "ScaleInCooldown": 600, "ScaleOutCooldown": 300, "DisableScaleIn": false}'
```
- The target metric is the average over **all** reader instances in the cluster, whether created by Auto Scaling or
  manually, including readers on custom endpoints, and excluding the writer (CloudWatch dimensions
  `DBClusterIdentifier` and `Role=READER`). Auto Scaling does not act on writer load, and only scales when all cluster
  instances are `available`.
- One Auto Scaling policy per target metric per cluster. The service-linked role is
  `AWSServiceRoleForApplicationAutoScaling_RDSCluster`. Aurora allows up to 15 readers per cluster (RDS quotas page:
  read replicas per primary, 15, not adjustable for Aurora).
- Use scheduled actions (`put-scheduled-action`) to pre-scale before known peaks; target tracking reacts to the metric.

## 3. Behaviour to understand
- Auto-scaled replicas have DB instance IDs prefixed `application-autoscaling-` (tag
  `application-autoscaling:resourceId`) and the promotion tier is the last priority, 15 by default, so failover prefers
  better-priority replicas such as manually created ones.
- The User Guide recommends the **reader endpoint** (and drivers such as the AWS JDBC Driver) so applications pick
  up new replicas.
- Scale-in removes only replicas that Aurora Auto Scaling created.
- Connections on a removed replica are dropped; clients must reconnect (pools with retry).

## 4. Choosing the metric
- Predefined: `RDSReaderAverageCPUUtilization`, `RDSReaderAverageDatabaseConnections`; custom metrics are supported through
  the CLI or API for any Aurora metric that changes in proportion to scaling.
- CPU works for compute-bound read workloads.
- Connections for connection-heavy workloads, but pools that open fixed connections per reader keep the average
  constant regardless of load.

## Gotchas
- Aurora global databases do not support Aurora Auto Scaling for secondary DB clusters.
- Cost: every replica is a full instance (new replicas use the writer's instance class); set a sane max and a cost alarm.

## Verify
- [ ] `describe-scalable-targets` and `describe-scaling-policies` show the policy; alarms created by target tracking exist in CloudWatch.
- [ ] Load test pushes reader CPU above target; a replica is added and joins the reader endpoint.
- [ ] After load drops and cooldown passes, the auto-scaled replica is removed; app reconnects cleanly.

## Checked
Date: 2026-10-27. Sources: Aurora User Guide Aurora.Integrating.AutoScaling and .AutoScaling.Add (metric
calculation, promotion tier 15, `application-autoscaling-` prefix, global database limitation, service-linked role,
predefined metrics, cooldowns); RDS quotas page (read replicas per primary); Application Auto Scaling botocore model
(`rds:cluster:ReadReplicaCount`, `RDSReaderAverageCPUUtilization`). Corrected the global database claim (secondary
clusters are NOT supported); removed the creation-time figure, Serverless v2 advice and custom endpoint membership claim.
Method: documentation only; no commands were run.
