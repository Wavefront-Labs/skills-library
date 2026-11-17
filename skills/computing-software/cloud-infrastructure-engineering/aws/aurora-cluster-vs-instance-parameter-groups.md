---
id: computing-software.cloud-infrastructure-engineering.aws.aurora-cluster-vs-instance-parameter-groups
name: aurora-cluster-vs-instance-parameter-groups
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aurora, cluster-parameter-group, db-parameter-group, pending-reboot, rds]
level: practitioner
status: docs-checked
description: "Put Aurora settings in the right place (DB cluster vs DB instance parameter groups), apply static vs dynamic changes, track pending-reboot and handle upgrades."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_WorkingWithParamGroups.html", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_WorkingWithDBClusterParamGroups.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aurora cluster vs instance parameter groups

## 1. Which group
| Group | Scope | What belongs there (User Guide) |
|---|---|---|
| DB cluster parameter group | every instance in the cluster | parameters tied to the physical layout of table data and to replication settings, which must be identical across the cluster |
| DB parameter group | one instance | settings such as memory usage that can differ per instance (instances often have different classes) |
Every Aurora cluster has a DB cluster parameter group that holds defaults for both cluster-level and instance-level
parameters; each instance inherits from it. Values set in a DB parameter group take precedence over the cluster
group for that instance. You cannot change values in a default parameter group. Use `describe-db-cluster-parameters`
and `describe-db-parameters` to see which group a given parameter appears in for your engine and version.

## 2. Create and attach
```bash
aws rds create-db-cluster-parameter-group --db-cluster-parameter-group-name apg-app \
  --db-parameter-group-family <FAMILY> --description "app cluster params"     # e.g. aurora-postgresql16 or aurora-mysql8.0
aws rds modify-db-cluster-parameter-group --db-cluster-parameter-group-name apg-app \
  --parameters "ParameterName=<PARAM>,ParameterValue=<VALUE>,ApplyMethod=pending-reboot"
aws rds modify-db-cluster --db-cluster-identifier app --db-cluster-parameter-group-name apg-app --apply-immediately
aws rds create-db-parameter-group --db-parameter-group-name apg-app-inst --db-parameter-group-family <FAMILY> --description inst
aws rds modify-db-instance --db-instance-identifier app-1 --db-parameter-group-name apg-app-inst --apply-immediately
```

## 3. Static vs dynamic
- `ApplyMethod=immediate` applies dynamic parameters without a restart; `pending-reboot` is the method for static ones.
- After changing a cluster parameter group, the User Guide says to reboot the primary (writer) instance first and then
  the readers; not rebooting can make a failover take longer. After associating a different cluster group, check the
  primary's `DBClusterParameterGroupStatus` for `pending-reboot` (older Aurora PostgreSQL versions also need each reader rebooted).
```bash
aws rds describe-db-clusters --db-cluster-identifier app --query 'DBClusters[].DBClusterMembers[].{id:DBInstanceIdentifier,status:DBClusterParameterGroupStatus}'
aws rds describe-db-cluster-parameters --db-cluster-parameter-group-name apg16-app --source user
```

## 4. Upgrades
Major version upgrades need parameter groups compatible with the new version: either the defaults for the new
version or custom groups you create first and test. `modify-db-cluster` accepts `--db-cluster-parameter-group-name`
and `--db-instance-parameter-group-name` together with `--engine-version` and `--allow-major-version-upgrade`.

## Verify
- [ ] The parameter value (checked with the engine's `SHOW` command) is the new value on each instance.
- [ ] No member shows `pending-reboot`.

## Checked
Date: 2026-10-27. Sources: Aurora User Guide pages USER_WorkingWithDBClusterParamGroups (two-level model, precedence),
USER_WorkingWithParamGroups.ModifyingCluster (reboot writer then readers), AssociatingCluster
(`DBClusterParameterGroupStatus`), the Aurora MySQL and PostgreSQL major version upgrade pages (parameter groups);
botocore `rds` model (`ModifyDBCluster` members `DBClusterParameterGroupName`, `DBInstanceParameterGroupName`,
`AllowMajorVersionUpgrade`). Corrected the reboot order (writer first, not last) and removed the per-parameter
scope table (examples not confirmed on a documentation page).
Method: documentation only; no commands were run.
