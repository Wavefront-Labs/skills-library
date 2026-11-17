---
id: computing-software.devops-ci-cd.rundeck.cluster-requirements
name: cluster-requirements
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, cluster-mode, shared-database, sticky-session, grails-serverurl]
level: advanced
status: docs-checked
description: "Checklist of shared resources an Enterprise Rundeck cluster needs: one database, load balancer with sticky sessions, shared log storage, common authentication and resource model."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/cluster/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Clustering is an Enterprise feature. Every member must share:

- Database: all instances use the same DB. Keys and project data must be stored in the DB (the default since 2.4.x), i.e. the storage facility is DB-backed.
- Load balancer: set `grails.serverURL` in each member's `rundeck-config.properties` to the load balancer URL, and enable sticky sessions.
- Log storage: all members share one location for execution logs. With the S3 log plugin use `com.rundeck.rundeckpro.amazon-s3` instead of `org.rundeck.amazon-s3`, which adds checkpoint storage so logs are viewable while an execution runs.
- Authentication: the same users and groups must be reachable from all instances.
- Resource model: projects need a node model every member can read, for example a shared file system, a script, or a REST endpoint.

Cluster features:
- Autotakeover: scheduled jobs are owned by the last member that modified them; with heartbeat and Autotakeover (2.1.0 and later), jobs from a downed member move to another automatically.
- Cluster remote execution policy: members can forward executions to other members.
- Replication plugin: active/passive setup where each member can have its own database.

Verify that every member appears in Cluster Manager.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Cluster Overview: shared database with DB-backed keys and project data, grails.serverURL plus sticky sessions, shared log storage and the com.rundeck.rundeckpro.amazon-s3 plugin id with checkpoint storage, common authentication, shared resource model, Autotakeover (2.1.0 and later), remote execution policy, replication plugin. Removed the unconfirmed per-node /health check.

Method: documentation only; no commands were run.
