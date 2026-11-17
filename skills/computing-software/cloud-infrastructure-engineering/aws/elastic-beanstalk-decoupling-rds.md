---
id: computing-software.cloud-infrastructure-engineering.aws.elastic-beanstalk-decoupling-rds
name: elastic-beanstalk-decoupling-rds
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elastic-beanstalk, eb-rds-decouple, rds, blue-green]
level: practitioner
status: docs-checked
description: "Decouple an RDS database from an Elastic Beanstalk environment (retain policy, decouple, pass connection settings) so environments can be replaced safely."
sources: ["https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.managing.db.html", "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.RDS.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decoupling an RDS database from Elastic Beanstalk

**Problem:** a database created inside the environment is tied to its lifecycle: terminating or
rebuilding the environment, or blue/green CNAME swaps, put the data at risk.

## 1. Decouple
1. Snapshot first: `aws rds create-db-snapshot --db-instance-identifier <EB_DB> --db-snapshot-identifier pre-decouple`.
2. Set the database **deletion policy** to `Retain` (the DB stays available and operational, decoupled from
   Beanstalk), or `Snapshot` (a snapshot is saved before Beanstalk terminates the DB). `Delete` terminates it.
   The policy applies both when you decouple the database and when you terminate the environment.
3. Decouple the database from the environment (console: Configuration, Database category). With `Retain`
   you can then point one or more environments at it as an external RDS instance.
4. An integrated database injects `RDS_HOSTNAME`, `RDS_PORT`, `RDS_DB_NAME`, `RDS_USERNAME` and `RDS_PASSWORD`
   environment properties; have your own connection properties in place before relying on a decoupled database.

## 2. Pass connection settings
```bash
aws elasticbeanstalk update-environment --environment-name app-prod --option-settings \
  Namespace=aws:elasticbeanstalk:application:environment,OptionName=DB_HOST,Value=<ENDPOINT> \
  Namespace=aws:elasticbeanstalk:application:environment,OptionName=DB_SECRET_ARN,Value=<SECRET_ARN>
```
Fetch the password from Secrets Manager at start-up (instance profile needs `GetSecretValue`).

## 3. Network
Keep the DB's security group rule allowing the environment's instance security group; reference the SG, not IPs.
A new environment needs that SG (or a shared app SG) added via the `SecurityGroups` option of the
`aws:autoscaling:launchconfiguration` namespace.

## 4. New environments
Create databases outside Elastic Beanstalk from the start (CloudFormation/Terraform), and pass endpoints as properties.

## Verify
- [ ] Terminating a cloned test environment leaves the DB intact.
- [ ] App reads the new properties; no `RDS_*` references remain in code.

## Checked
2026-10-28: Confirmed against the Beanstalk Developer Guide page "Adding a database to your Elastic Beanstalk environment" (using-features.managing.db) and the RDS how-to page: the Snapshot/Delete/Retain deletion policies and their meaning, that a decoupled database can be used by environments as an external RDS instance, that decoupling enables blue/green deployments, and the RDS_* environment property names. The sources entry using-features.decoupling.db.html returned an empty stub, so it was replaced. Read end to end. Removed: the deletion protection step, the claim about the CloudFormation stack, and the claim that the environment loses the RDS_* properties.

Method: documentation only; no commands were run.
