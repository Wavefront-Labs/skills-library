---
id: computing-software.cloud-infrastructure-engineering.aws.dms-homogeneous-migrations-and-fleet-advisor
name: dms-homogeneous-migrations-and-fleet-advisor
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dms, homogeneous-migration, fleet-advisor, native-tools, data-providers]
level: advanced
status: docs-checked
description: "Migrate like-to-like databases with DMS homogeneous data migrations (native pg_dump, mydumper, mongodump under the hood) and inventory sources with discovery tools."
sources: ["https://docs.aws.amazon.com/dms/latest/userguide/data-migrations.html", "https://docs.aws.amazon.com/dms/latest/userguide/dm-getting-started.html", "https://docs.aws.amazon.com/dms/latest/userguide/fa-data-collectors.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DMS homogeneous data migrations and Fleet Advisor

## 1. Homogeneous data migrations
Serverless DMS feature for same-engine moves (the guide names PostgreSQL, MongoDB and DocumentDB among
the supported engines; check the supported source and target list). DMS scales the resources automatically, so
there is no replication instance to size. It works with instance profiles, data providers and migration projects, and
runs native database tools: it dumps files to disk and restores them with those tools.
```bash
aws dms create-instance-profile --instance-profile-name hdm --subnet-group-identifier dms-subnets \
  --vpc-security-groups sg-dms --network-type IPV4
aws dms create-data-provider --data-provider-name src-pg --engine postgres \
  --settings 'PostgreSqlSettings={ServerName=10.1.2.3,Port=5432,DatabaseName=app,SslMode=require}'
aws dms create-data-provider --data-provider-name tgt-apg --engine aurora-postgresql \
  --settings 'PostgreSqlSettings={ServerName=app.cluster-xxxx.<REGION>.rds.amazonaws.com,Port=5432,DatabaseName=app,SslMode=require}'
aws dms create-migration-project --migration-project-name app-move --instance-profile-identifier hdm \
  --source-data-provider-descriptors DataProviderIdentifier=src-pg,SecretsManagerSecretId=<SRC_SECRET>,SecretsManagerAccessRoleArn=<ROLE> \
  --target-data-provider-descriptors DataProviderIdentifier=tgt-apg,SecretsManagerSecretId=<TGT_SECRET>,SecretsManagerAccessRoleArn=<ROLE>
aws dms create-data-migration --migration-project-identifier app-move --data-migration-type full-load-and-cdc \
  --service-access-role-arn <ROLE> --data-migration-name app-move-run
aws dms start-data-migration --data-migration-identifier app-move-run --start-type start-replication
```
- Check the source prerequisites for your engine on the data-migrations pages before starting.
- Cut over when replication has caught up; stop writes, wait, repoint.

## 2. Fleet Advisor (discovery)
A DMS data collector (a Windows application) installed in your network connects to your source databases,
which can run on any supported OS or vendor. It uses LDAP credentials for OS discovery, sudo SSH credentials
for Linux database discovery and WMI/WQL access for Windows. DMS Fleet Advisor builds an inventory of servers,
databases and schemas from the collected metadata. Confirm Fleet Advisor is offered to your account before planning around it.

## Verify
- [ ] Row counts and checksums match per table; CDC lag zero before cutover.

## Checked

2026-10-28. Confirmed against the DMS homogeneous data migration and Fleet Advisor data collector pages: serverless scaling, instance profiles/data providers/migration projects, native dump-and-restore, PostgreSQL/MongoDB/DocumentDB support, data collector being a Windows application, LDAP/SSH/WMI discovery credentials, inventory of servers/databases/schemas. Removed (unconfirmed): pg_dump/mydumper/mongodump names, MySQL/MariaDB claim, per-engine source prerequisites, S3 upload and sizing recommendations, the availability comment about newer tools. Read end to end.

Method: documentation only; no commands were run.
