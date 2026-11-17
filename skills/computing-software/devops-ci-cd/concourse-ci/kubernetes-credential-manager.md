---
id: computing-software.devops-ci-cd.concourse-ci.kubernetes-credential-manager
name: kubernetes-credential-manager
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [kubernetes, credential-manager, secrets, rbac, namespace, serviceaccount, rolebinding]
level: practitioner
status: docs-checked
description: "Read Concourse credentials from Kubernetes secrets: in-cluster or kubeconfig, per-team namespaces, ServiceAccount, ClusterRole and RoleBinding RBAC, lookup order, prefix, suffix."
sources:
  - https://concourse-ci.org/docs/operation/creds/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable with `CONCOURSE_KUBERNETES_IN_CLUSTER=true` or `CONCOURSE_KUBERNETES_CONFIG_PATH=~/.kube/config` on the web node.

**RBAC.** The web node must read secrets in the namespaces where each team's secrets live, for example `concourse-team-a` and `concourse-team-b`. The documented pattern: a `ServiceAccount` named `web`; a `ClusterRole` `read-secrets` with `resources: ["secrets"]` and `verbs: ["get"]`; and one `RoleBinding` per team namespace binding that role to the service account (a per-namespace binding of a cluster role restricts effective permissions to that namespace); then set `serviceAccountName: web` on the web Deployment's pod spec.

**Lookup.** For `((foo))` in a team's namespace `concourse-TEAM_NAME`, first a secret named `PIPELINE_NAME.foo`, then one named `foo`. The key read is `value`, and JSON content gives nested fields: `((foo.bar))`. One-off tasks only use the team namespace.

**Customise:**
```properties
CONCOURSE_KUBERNETES_NAMESPACE_SHARED_SUFFIX=shared-suffix
CONCOURSE_KUBERNETES_NAMESPACE_PREFIX=some-other-prefix-
```
The shared suffix with the default prefix gives namespace `concourse-shared-suffix`, which must exist. Shared credentials skip team and pipeline namespacing, so use with care. The prefix replaces `concourse-`.

Note the page's YAML examples use older API versions such as `rbac.authorization.k8s.io/v1beta1`; check current versions for your cluster.

## Checked

2026-11-04. Env vars, RBAC objects and lookup order confirmed on the Kubernetes credential manager page; the API version caveat is an observation about the page's examples.

Method: documentation only; no commands were run.
