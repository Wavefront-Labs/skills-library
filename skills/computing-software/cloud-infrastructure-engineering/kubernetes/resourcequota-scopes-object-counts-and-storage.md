---
id: computing-software.cloud-infrastructure-engineering.kubernetes.resourcequota-scopes-object-counts-and-storage
name: resourcequota-scopes-object-counts-and-storage
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, resourcequota, quota-scopes, scopeselector, object-count-quota, storage-quota, priorityclass-quota, multi-tenancy]
level: practitioner
status: docs-checked
description: "Write ResourceQuotas beyond CPU/memory: object counts (count/<resource>), per-StorageClass storage quotas, and scopeSelector for PriorityClass and BestEffort."
sources: ["https://kubernetes.io/docs/concepts/policy/resource-quotas/", "https://kubernetes.io/docs/concepts/policy/resource-quotas/#quota-scopes", "https://kubernetes.io/docs/concepts/policy/resource-quotas/#storage-resource-quota", "https://kubernetes.io/docs/concepts/policy/resource-quotas/#resource-quota-per-priorityclass"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ResourceQuota: scopes, object counts and storage

## Object-count quotas
```yaml
apiVersion: v1
kind: ResourceQuota
metadata: {name: objects, namespace: team-a}
spec:
  hard:
    pods: "200"
    services.loadbalancers: "1"        # each costs a cloud LB
    services.nodeports: "0"
    persistentvolumeclaims: "20"
    count/deployments.apps: "50"
    count/jobs.batch: "100"
    count/secrets: "200"
    count/configmaps: "200"
    count/widgets.example.com: "10"    # CRDs too
```
Object counts protect the control plane (etcd size, controller load) from runaway
generators and CI leaking objects.

## Storage quotas
```yaml
  hard:
    requests.storage: 2Ti                                           # all PVCs
    gold.storageclass.storage.k8s.io/requests.storage: 500Gi        # per StorageClass
    gold.storageclass.storage.k8s.io/persistentvolumeclaims: "5"
    bronze.storageclass.storage.k8s.io/requests.storage: 0          # forbid a class entirely
    requests.ephemeral-storage: 200Gi
    limits.ephemeral-storage: 400Gi
```
## Scopes
```yaml
spec:
  hard: {pods: "10", requests.cpu: "20"}
  scopeSelector:
    matchExpressions:
    - {scopeName: PriorityClass, operator: In, values: [high-priority]}
```
Scopes: `Terminating` / `NotTerminating` (has `activeDeadlineSeconds` or not), `BestEffort` /
`NotBestEffort`, `PriorityClass`, `CrossNamespacePodAffinity`, `VolumeAttributesClass`.
A quota with a scope only counts matching objects.

### Restrict a PriorityClass to some namespaces
Make expensive classes "unusable unless granted": configure the apiserver admission
`ResourceQuota` plugin with `limitedResources` for `pods` matching that PriorityClass, then only
namespaces that have an explicit quota for it can use it:
```yaml
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
      - {scopeName: PriorityClass, operator: In, values: [cluster-services]}
```

## Inspect
```bash
kubectl describe quota -n team-a      # Used vs Hard for each key
kubectl get resourcequota -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,USED:.status.used
```

## Verify
- [ ] Creating the 2nd LoadBalancer Service in team-a fails with `exceeded quota`.
- [ ] A pod with a restricted PriorityClass is rejected in namespaces without a matching quota.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Object count syntax `count/<resource>.<group>`, specialized names (`services.loadbalancers`, `services.nodeports`,
  `persistentvolumeclaims`), per-StorageClass keys `<class>.storageclass.storage.k8s.io/requests.storage` and
  `.../persistentvolumeclaims`, `requests.ephemeral-storage` and `limits.ephemeral-storage`: resource-quotas page.
- Scope list (`Terminating`, `NotTerminating`, `BestEffort`, `NotBestEffort`, `PriorityClass`, `CrossNamespacePodAffinity`,
  `VolumeAttributesClass`) and `scopeSelector` syntax: resource-quotas page.
- `AdmissionConfiguration` with `ResourceQuotaConfiguration` and `limitedResources` / `matchScopes` for PriorityClass:
  resource-quotas page (identical structure).
- Removed: the statement about PVC expansion counting against quota, which the page does not make.

Method: documentation only; no commands were run.
