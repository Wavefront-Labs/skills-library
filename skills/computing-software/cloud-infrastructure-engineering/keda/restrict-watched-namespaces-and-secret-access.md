---
id: computing-software.cloud-infrastructure-engineering.keda.restrict-watched-namespaces-and-secret-access
name: restrict-watched-namespaces-and-secret-access
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [watch-namespace, keda-restrict-secret-access, cluster-role, secrets-rbac, least-privilege]
level: advanced
status: docs-checked
description: "Limit which namespaces the KEDA operator watches and remove cluster-wide secret read access with WATCH_NAMESPACE and KEDA_RESTRICT_SECRET_ACCESS."
sources:
  - https://keda.sh/docs/2.17/operate/cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Namespace scope: by default KEDA watches all namespaces. Set the `WATCH_NAMESPACE` environment variable to one namespace, a comma-separated list, or an empty string for all. ScaledObjects and ScaledJobs created in other namespaces are ignored by the operator.

```yaml
- env:
    WATCH_NAMESPACE: keda,production
```

Secret access: by default KEDA needs a cluster role granting `get`, `list`, `watch` on `external`, `pods`, `secrets` and `services` in the core API group. That means permission to read secrets in every namespace, a risk especially in production.

To confine secret reading to the KEDA namespace, set the following on both the Operator and the Metrics Server:

```yaml
env:
  - name: KEDA_RESTRICT_SECRET_ACCESS
    value: "true"
```

You can then omit `secrets` from the cluster role. Consequence: a `TriggerAuthentication` that uses secrets can no longer be used for your triggers; `ClusterTriggerAuthentication` still works because by default its secrets are read from the KEDA namespace.

## Checked

2026-11-03. Confirmed on the 2.17 Operate Cluster page: WATCH_NAMESPACE, cluster role rules, KEDA_RESTRICT_SECRET_ACCESS. Removed: a multi-tenant recommendation the page does not make.

Method: documentation only; no commands were run.
