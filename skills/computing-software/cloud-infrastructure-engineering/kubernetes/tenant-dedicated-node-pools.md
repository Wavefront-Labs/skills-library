---
id: computing-software.cloud-infrastructure-engineering.kubernetes.tenant-dedicated-node-pools
name: tenant-dedicated-node-pools
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-tenancy-isolation, tenant-node-pools, taints-tolerations, podnodeselector, podtolerationrestriction]
level: practitioner
status: docs-checked
description: "Give tenants dedicated node pools with taints and labels, and force each namespace's pods onto its pool with admission plugins or policy so tenants cannot opt out."
sources: ["https://kubernetes.io/docs/concepts/security/multi-tenancy/", "https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#podnodeselector", "https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#podtolerationrestriction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dedicated node pools per tenant

Node isolation stops noisy neighbours and limits blast radius of a container escape to one
tenant's nodes.

## Nodes
```bash
kubectl label nodes -l pool=tenant-a tenant=a
kubectl taint nodes -l pool=tenant-a tenant=a:NoSchedule
```
Use the node group or Karpenter NodePool to apply these at creation.

## Force placement (tenants must not choose)
Option 1, built-in admission plugins (`--enable-admission-plugins=...,PodNodeSelector,PodTolerationRestriction`):
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: tenant-a
  annotations:
    scheduler.alpha.kubernetes.io/node-selector: "tenant=a"
    scheduler.alpha.kubernetes.io/defaultTolerations: '[{"key":"tenant","operator":"Equal","value":"a","effect":"NoSchedule"}]'
    scheduler.alpha.kubernetes.io/tolerationsWhitelist: '[{"key":"tenant","operator":"Equal","value":"a"}]'
```
Option 2, admission policy: a mutating policy that adds the nodeSelector and toleration from a namespace label (MutatingAdmissionPolicy is stable from Kubernetes 1.36) plus a validating policy (ValidatingAdmissionPolicy is stable from 1.30) that rejects other tenants' tolerations, or an equivalent policy engine.

## Don't forget
- DaemonSets (log agents, CNI) need tolerations for all tenant taints.
- Tenants must not get RBAC to patch namespaces (they could change the annotations) or nodes.
- Use separate cloud IAM roles per pool so node credentials are tenant-scoped.

## Verify
```bash
kubectl run t -n tenant-a --image=busybox --restart=Never -- sleep 60
kubectl get pod t -n tenant-a -o jsonpath='{.spec.nodeName}' | xargs kubectl get node -L tenant
```
A pod in tenant-a with a toleration for tenant b is rejected.

## Checked

2026-10-27. Release: Kubernetes v1.37 docs (kubernetes/website main), October 2026
- Confirmed in the admission controllers page the `PodNodeSelector` plugin with annotation `scheduler.alpha.kubernetes.io/node-selector` (disabled by default) and the `PodTolerationRestriction` plugin with annotations `scheduler.alpha.kubernetes.io/defaultTolerations` and `scheduler.alpha.kubernetes.io/tolerationsWhitelist`, which rejects pods whose tolerations conflict.
- Confirmed in the multi-tenancy page that tenant nodes are isolated with taints and matching tolerations, and the stable stages of ValidatingAdmissionPolicy (1.30) and MutatingAdmissionPolicy (1.36). Removed the Kyverno-specific claim and the pinned busybox tag.

Method: documentation only; no commands were run.
