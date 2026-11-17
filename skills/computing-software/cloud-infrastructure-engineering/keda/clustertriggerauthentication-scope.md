---
id: computing-software.cloud-infrastructure-engineering.keda.clustertriggerauthentication-scope
name: clustertriggerauthentication-scope
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [clustertriggerauthentication, keda-cluster-object-namespace, shared-credentials, authentication-scope]
level: practitioner
status: docs-checked
description: "Share one set of KEDA credentials across namespaces with ClusterTriggerAuthentication and learn where its Secrets must live."
sources:
  - https://keda.sh/docs/2.17/concepts/authentication/
  - https://keda.sh/docs/2.17/operate/cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
This is the third pattern KEDA lists for authentication, re-using global credentials, next to per-ScaledObject configuration and the namespaced TriggerAuthentication.
A `TriggerAuthentication` can be used only by ScaledObjects in its own namespace. To share one credential set between scalers in many namespaces, create a `ClusterTriggerAuthentication`. Its spec is almost identical, but it has no `metadata.namespace`:

```yaml
apiVersion: keda.sh/v1alpha1
kind: ClusterTriggerAuthentication
metadata:
  name: {cluster-trigger-authentication-name}
spec:
  # As before ...
```

Reference it by adding `kind` to the trigger's `authenticationRef`:

```yaml
authenticationRef:
  name: {cluster-trigger-authentication-name}
  kind: ClusterTriggerAuthentication
```

Where secrets come from: by default, Secrets loaded from a `secretTargetRef` in a cluster-scoped object must be in the namespace where KEDA is deployed, usually `keda`. Override it by setting the `KEDA_CLUSTER_OBJECT_NAMESPACE` environment variable on the `keda-operator` container.

Security interaction: if you set `KEDA_RESTRICT_SECRET_ACCESS=true` (see restrict-watched-namespaces-and-secret-access), namespaced TriggerAuthentications that use secrets stop working but `ClusterTriggerAuthentication` still can. The admission webhook also rejects an empty identity ID when a cluster or namespaced authentication overrides the default `identityId`.

## Checked

2026-11-03. Confirmed on the 2.17 Authentication and Operate Cluster pages: cluster scope, kind field, KEDA_CLUSTER_OBJECT_NAMESPACE, KEDA_RESTRICT_SECRET_ACCESS, and the identity ID rule on the webhook page.

Method: documentation only; no commands were run.
