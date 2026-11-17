---
id: computing-software.devops-ci-cd.spinnaker.kubernetes-provider-setup
name: kubernetes-provider-setup
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [kubernetes, provider, kubeconfig, kubectl, rbac, service-account, namespaces, accounts]
level: practitioner
status: docs-checked
description: "Prepare the Kubernetes provider: kubeconfig and kubectl needs, optional service account, RBAC ClusterRole vs Role per namespace, and the clouddriver-local.yml account block."
sources:
  - https://spinnaker.io/docs/setup/install/providers/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Kubernetes provider fully supports manifest-based deployments and is the recommended way to deploy to Kubernetes. The page calls it the Kubernetes V2 provider, the standard Kubernetes provider for Spinnaker.

A Spinnaker Account maps to a credential that authenticates against a cluster. Two prerequisites:
- a `kubeconfig` file giving read/write access to every resource Spinnaker should manage;
- the `kubectl` binary, which is installed alongside Spinnaker. Spinnaker relies on it for all API access because only kubectl fully supports things like 3-way merges on apply and API discovery, so any auth method kubectl supports works.

**Optional service account.** The page applies a ClusterAdmin service account manifest, reads its token, and adds a token user to your kubeconfig context; it says more restrictive roles can be used.

**RBAC.** The page provides a `ClusterRole` (get/list on namespaces, configmaps, events and a few other resources; create/delete/patch/update/watch and more on pods, services, secrets, deployments, replicasets and ingresses), a binding and a ServiceAccount in namespace `spinnaker`. If you limit Spinnaker to explicit `namespaces`, use `Role` and `RoleBinding` in each namespace instead, and you must specify those namespaces when adding the account. If you specify no namespaces, Spinnaker attempts to list all namespaces, which requires a cluster-wide role.

**Adding the account.** Add to `clouddriver-local.yml` a `kubernetes` block with `enabled: true` and an entry under `accounts` that has `name`, `kubeconfigFile`, optional `kubectlExecutable`, `cacheIntervalSeconds`, `namespaces` and `permissions` (`READ` and `WRITE` role lists). The page's example also sets `loadNamespacesInAccount: false` and `verifyAccountHealth: false`. Then enable artifact support.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Kubernetes V2 Provider page. Confirmed the kubectl dependency, service account steps, RBAC contents, namespace behaviour and the clouddriver-local.yml account block. Removed the V1 removal and migration claims and the "Wait for Manifest to Stabilize" timeout remark, which the page does not state.
