---
id: computing-software.messaging-and-integration.strimzi.prerequisites-and-oc
name: prerequisites-and-oc
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [deployment-prerequisites, kubernetes-version, kubectl, oc]
level: intro
status: docs-checked
description: "Check cluster version and tooling before deploying Strimzi."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Strimzi deployment prerequisites

**Goal:** confirm the cluster and CLI meet Strimzi requirements.

The deploying guide for this release lists:

- A Kubernetes cluster at version **1.32 or later**.
- `kubectl` installed and configured for the running cluster.

Strimzi also supports some OpenShift-specific features where no standard Kubernetes equivalent exists. On OpenShift, `oc` is an alternative to `kubectl`; in almost all cases the example commands work by replacing the command name, with options and arguments unchanged:

```bash
kubectl apply -f <your_file>
oc apply -f <your_file>
```

The exception is cluster management: `oc` uses `oc adm` subcommands where `kubectl` does not. For example, the `oc` equivalent of `kubectl taint` is `oc adm taint`.

The cluster user running the guide's commands also needs rights to manage RBAC and CRDs.

```bash
kubectl version
kubectl get nodes
```

**Checklist**

1. Verify the server version is 1.32 or later.
2. Verify `kubectl` points at the intended cluster context.
3. On OpenShift, use `oc adm` for administrative subcommands.

## Checked

Method: docs-checked 2026-11-09 against the Strimzi deploying guide (Deployment prerequisites, oc and kubectl commands). The upgrade-guide version claim was dropped because that page was not read.
