---
id: computing-software.cloud-infrastructure-engineering.kubernetes.crossnamespacepodaffinity-quota-scope
name: crossnamespacepodaffinity-quota-scope
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, resourcequota, crossnamespacepodaffinity, pod-affinity, multi-tenancy, admission-configuration]
level: practitioner
status: docs-checked
description: "Stop tenants from using pod affinity terms that target other namespaces by combining the CrossNamespacePodAffinity quota scope with limitedResources."
sources: ["https://kubernetes.io/docs/concepts/policy/resource-quotas/#cross-namespace-pod-affinity-scope", "https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#namespace-selector"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CrossNamespacePodAffinity quota scope

Pod (anti-)affinity terms with `namespaces` or `namespaceSelector` let one tenant's pods react to
another tenant's pods, for example anti-affinity that blocks scheduling next to them. The quota
scope (stable since v1.24) counts pods using such terms.

## Deny in one namespace
```yaml
apiVersion: v1
kind: ResourceQuota
metadata: {name: no-cross-ns-affinity, namespace: tenant-a}
spec:
  hard: {pods: "0"}
  scopeSelector:
    matchExpressions:
    - {scopeName: CrossNamespacePodAffinity, operator: Exists}
```

## Deny everywhere unless allowed
Make the scope a limited resource, so pods using it are rejected in any namespace with no
matching quota:
```yaml
# --admission-control-config-file on kube-apiserver
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: ResourceQuota
  configuration:
    apiVersion: apiserver.config.k8s.io/v1
    kind: ResourceQuotaConfiguration
    limitedResources:
    - resource: pods
      matchScopes:
      - {scopeName: CrossNamespacePodAffinity, operator: Exists}
```
Pods may then use `namespaces` or `namespaceSelector` only in namespaces that have a quota with this
scope and a hard `pods` limit at least equal to the number of pods using those fields, for example `pods: "50"`.

## Verify
A pod with `podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[].namespaceSelector: {}`
is rejected by quota admission in tenant-a, while plain same-namespace affinity is accepted.

## Checked
2026-10-23, against the Kubernetes website resource-quotas page (CrossNamespacePodAffinity scope, v1.24 stable): both manifests, the `scopeName`/`operator: Exists` selector, `--admission-control-config-file`, `limitedResources`/`matchScopes`, and the rule that a quota with hard limit >= the number of pods using the fields is needed.
Method: documentation only; no commands were run.
