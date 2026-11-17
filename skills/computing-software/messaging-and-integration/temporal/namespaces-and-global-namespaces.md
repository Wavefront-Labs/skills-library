---
id: computing-software.messaging-and-integration.temporal.namespaces-and-global-namespaces
name: namespaces-and-global-namespaces
category: computing-software
field: messaging-and-integration
product: temporal
tags: [namespace, global-namespace, failover, multi-cluster, isolation, default-namespace, workflow-id]
level: intro
status: docs-checked
description: "Temporal namespaces as the unit of isolation, the default namespace, Workflow ID uniqueness, and global namespaces with failover version and NamespaceNotActiveError."
sources:
  - https://docs.temporal.io/namespaces
  - https://docs.temporal.io/global-namespace
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Namespace is Temporal's unit of isolation. Task Queues and Workflow Executions belong to one.

What it governs:
- Workflow ID uniqueness holds within a Namespace; other Namespaces may reuse an ID.
- Heavy traffic in one Namespace does not affect others on the same Service.
- Retention Period and Archival destination are set per Namespace.
- If none is named, SDKs and the CLI use `default`; any other must be created before a Client uses it.
- Self-hosted access control is a custom Authorizer on the Frontend Service; Cloud uses role-based access.
- Namespaces are isolated by default; Nexus is the controlled path for calling another Namespace.
- One Namespace is still multi-tenant, so teams sharing it must coordinate Workflow ID and Task Queue naming.

Moving between self-hosting and Temporal Cloud needs no code changes.

Global Namespace: a Namespace that exists across Clusters under Multi-Cluster Replication. It can replicate to any number of Clusters but only one is active at a time. Rules:
- Workers must poll the Global Namespace on all Clusters; standby Workers idle until failover.
- Only the active Cluster dispatches Tasks.
- A failover version resolves conflicts if failover is triggered on two Clusters at once.
- API calls to a non-active Cluster fail with `NamespaceNotActiveError` naming the active Cluster; applications must call the right one.
- Activities become at-least-once, not at-most-once as in regular Namespaces.

## Checked

2026-11-08. Read in full: the Namespace and Global Namespace pages (docs.temporal.io/namespaces, docs.temporal.io/global-namespace). Every remaining claim matches those pages. Removed: the CLI registration command, which the pages do not give.

Method: documentation only; no commands were run.
