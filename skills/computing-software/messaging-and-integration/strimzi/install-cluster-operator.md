---
id: computing-software.messaging-and-integration.strimzi.install-cluster-operator
name: install-cluster-operator
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [cluster-operator-install, kubectl-apply, install-yaml]
level: practitioner
status: docs-checked
description: "Install the Cluster Operator from the release installation files."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing the Cluster Operator

**Goal:** deploy the Cluster Operator with one command.

The first step of any Strimzi deployment is the Cluster Operator. From the extracted release, run:

```bash
kubectl apply -f ./install/cluster-operator
```

This creates the operator Deployment and ConfigMap, the Strimzi CRDs, RBAC resources (ClusterRole, ClusterRoleBinding, RoleBinding) and a ServiceAccount.

Cluster-scoped resources (CustomResourceDefinition, ClusterRole, ClusterRoleBinding) need administrator privileges to install. Review the ClusterRole specifications beforehand to be sure they do not grant unnecessary privileges.

After installation the operator runs as a regular Deployment. Any standard user with access to the Deployment can configure it, and an administrator can grant users the privileges to manage Strimzi custom resources.

By default one replica is deployed. You can add replicas with leader election so extra operators stand by.

Warning from the docs: although the operator can watch multiple namespaces, each watched namespace should contain only one instance of a specific component type, such as one Kafka cluster.

**Checklist**

1. Review the ClusterRole before applying.
2. Apply `./install/cluster-operator` as an admin.
3. Confirm the Deployment is ready with `kubectl get deployment`.

## Checked

Method: docs-checked 2026-11-09 against the Strimzi deploying guide (Deploying the Cluster Operator and the deployment-conflict warning). The readiness command is generic and not from the page.
