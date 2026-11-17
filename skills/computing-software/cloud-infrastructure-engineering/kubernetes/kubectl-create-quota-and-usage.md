---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-create-quota-and-usage
name: kubectl-create-quota-and-usage
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, resourcequota, kubectl-create-quota, quota, object-count-quota]
level: practitioner
status: docs-checked
description: "Create ResourceQuotas imperatively with kubectl create quota, read used versus hard usage, and compute remaining headroom per namespace."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_quota/", "https://kubernetes.io/docs/concepts/policy/resource-quotas/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl create quota and reading usage

## Create
```bash
kubectl create quota compute -n team-a \
  --hard=requests.cpu=8,requests.memory=16Gi,limits.memory=32Gi,pods=50
kubectl create quota objects -n team-a \
  --hard=count/deployments.apps=20,count/secrets=100,services.loadbalancers=2,persistentvolumeclaims=10
kubectl create quota besteffort -n team-a --hard=pods=5 --scopes=BestEffort
```
`count/<resource>.<group>` works for any namespaced resource, including CRDs.

## Read usage
```bash
kubectl get quota -n team-a
kubectl describe quota compute -n team-a
# Resource         Used   Hard
# requests.cpu     6500m  8
kubectl get resourcequota -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,USED:.status.used,HARD:.status.hard
```

## Gotchas
- Neither contention nor quota changes affect resources that already exist.
- Compute quotas (`requests.*`, `limits.*`, `pods`) count only pods in a non-terminal state; a pod is terminal when `.status.phase` is Failed or Succeeded.

## Checked
Checked 2026-10-24 against the kubectl create quota source (main) and the Resource Quotas page (v1.37): `--hard` and `--scopes` flags, `count/<resource>.<group>` and `count/<resource>` syntax, `services.loadbalancers`, `persistentvolumeclaims`, BestEffort scope, non-terminal pod counting, existing resources unaffected. Removed the jq pipeline, the kube-state-metrics query and unconfirmed lag and precedence claims.
Method: documentation only; no commands were run.
