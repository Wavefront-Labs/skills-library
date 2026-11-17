---
id: computing-software.devops-ci-cd.backstage.deploy-scaling
name: deploy-scaling
category: computing-software
field: devops-ci-cd
product: backstage
tags: [scaling, multiple-instances, split-backends, backstage]
level: advanced
status: docs-checked
description: "Scale Backstage by running identical instances on shared resources or by splitting the backend into services."
sources:
  - https://backstage.io/docs/deployment/scaling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Three approaches are described.

1. Multiple identical instances. Deploy several copies and spread requests across them. The one requirement is that all instances share the same external resources: the database, and any optional caching or search services. The backend plugins coordinate through the database to share state and work.
2. Split the backend into several services, each running a different set of plugins. This is the advanced option. You must route requests to the correct backend by plugin id, both at ingress and for internal traffic between backends, by creating a custom implementation of the `DiscoveryService` interface.
3. Replicate across regions. There is no built-in support, and it usually makes sense only for individual backend plugins.

```yaml
# Deployment excerpt: several identical replicas
spec:
  replicas: 3
```

Practical implication:

- All instances must share the same external resources: the database and any optional caching or search services.

The backend system docs describe how to separate a deployment into multiple backend instances.

## Checked

2026-11-03. Confirmed on the Scaling Backstage Deployments page: the three approaches (identical instances sharing external resources, splitting the backend by plugin and routing by plugin id via a custom `DiscoveryService`, and replicating across regions with no built-in support). Removed: the SQLite, Lunr, TechDocs publisher and shared-cache bullets, the duplicate scheduled task claim and the sequencing advice, none of which the page states.

Method: documentation only; no commands were run.
