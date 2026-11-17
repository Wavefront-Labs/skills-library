---
id: computing-software.cloud-infrastructure-engineering.aws.rds-extended-support-and-engine-end-of-life
name: rds-extended-support-and-engine-end-of-life
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds, extended-support, engine-end-of-life, major-version-upgrade, aurora]
level: practitioner
status: docs-checked
description: "Handle RDS and Aurora major version end of standard support: Extended Support enrolment and charges, opting out at creation, and planning upgrades before the date."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/extended-support.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/extended-support-creating-db-instance.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDS Extended Support and engine end of life

## 1. What happens at end of standard support
Instances and clusters created or restored with Extended Support enabled (the default in the CLI and API; the
console checkbox is not selected by default) are **automatically enrolled in Extended Support**, which is
charged, for up to 3 years past the end of standard support (critical and high CVE fixes and critical bug
fixes). After that period RDS upgrades the major version automatically. Check the pricing page for current
charges. Enrolment can also be changed on an existing resource by modifying `EngineLifecycleSupport` (at cluster
level for Aurora and Multi-AZ DB clusters); disabling it on a resource already past standard support triggers an
automatic upgrade to the next supported major version.

## 2. Find exposure
```bash
aws rds describe-db-instances --query 'DBInstances[].{id:DBInstanceIdentifier,engine:Engine,ver:EngineVersion,ls:EngineLifecycleSupport}'
aws rds describe-db-clusters --query 'DBClusters[].{id:DBClusterIdentifier,engine:Engine,ver:EngineVersion,ls:EngineLifecycleSupport}'
aws rds describe-db-major-engine-versions --engine postgres \
  --query 'DBMajorEngineVersions[].{v:MajorEngineVersion,life:SupportedEngineLifecycles}'
```
`SupportedEngineLifecycles` lists `open-source-rds-standard-support` and `open-source-rds-extended-support` with
start and end dates per major version.

## 3. Opt out at creation, restore or modify
```bash
aws rds create-db-instance ... --engine-lifecycle-support open-source-rds-extended-support-disabled
aws rds restore-db-instance-from-db-snapshot ... --engine-lifecycle-support open-source-rds-extended-support-disabled
aws rds modify-db-instance --db-instance-identifier <id> --engine-lifecycle-support open-source-rds-extended-support-disabled
```
Opted-out resources are upgraded automatically on or shortly after the end of standard support date. Creating a new
instance on a version already past standard support with the disabled value always fails. The value to enrol is
`open-source-rds-extended-support`, which is also the default when the option is omitted, so automation that does not
set it (CloudFormation, restores) enrols by default.

## 4. Upgrade plan
1. Inventory and dates (engine release calendar).
2. Test on a clone: extensions/plugins, deprecated syntax, query plans.
3. Use **Blue/Green Deployments** for minimal-downtime major upgrades (`create-blue-green-deployment --target-engine-version`).
4. Upgrade parameter groups to the new family first.
5. Upgrade before the date; Extended Support is a bridge, not a plan.

## Verify
- [ ] No production databases with `EngineLifecycleSupport` showing extended support without an approved exception.

## Checked
Date: 2026-10-27. Source: RDS User Guide extended-support and extended-support-creating-db-instance pages, and the
botocore `rds` service model (CreateDBInstance, ModifyDBInstance, RestoreDBInstanceFromDBSnapshot,
DescribeDBMajorEngineVersions, CreateBlueGreenDeployment `TargetEngineVersion`). Confirmed: the 3-year limit, default
enrolment in CLI/API, the two parameter values, `SupportedEngineLifecycles` enum values, modify behaviour. Removed
price and usage-type claims (pricing page not readable).
Method: documentation only; no commands were run.
