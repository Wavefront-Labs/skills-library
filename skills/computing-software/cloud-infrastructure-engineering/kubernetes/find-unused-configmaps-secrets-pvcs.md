---
id: computing-software.cloud-infrastructure-engineering.kubernetes.find-unused-configmaps-secrets-pvcs
name: find-unused-configmaps-secrets-pvcs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, unused-resources, kor, cleanup, configmaps, persistentvolumeclaims]
level: practitioner
status: docs-checked
description: "Find ConfigMaps, Secrets, PVCs and other objects nothing references, using kor or kubectl and jq, and remove them safely."
sources: ["https://github.com/yonahd/kor", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/#delete", "https://kubernetes.io/docs/reference/kubectl/jsonpath/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding unused ConfigMaps, Secrets and PVCs

## kor
```bash
kor all -n shop                       # -n = --include-namespaces; unused objects of every supported kind
kor configmap --exclude-namespaces kube-system,kube-public   # all namespaces except these
kor secret --exclude-namespaces kube-system,kube-public
kor pvc -n shop -o json               # table (default), json or yaml
kor all -n shop --show-reason         # why each object is considered unused
kor configmap -n shop --delete        # prompts per object; keep for after review
```
kor checks ConfigMaps and Secrets used by pods through volumes and environment variables, Secrets
used by Ingress TLS and ServiceAccounts, and PVCs used in pods. Its documented false positives are
objects that a consumer loads without naming them in its spec (dynamically loaded dashboards,
policies, CRD-driven configs).

## Manual check for one namespace
```bash
NS=shop
used=$(kubectl get pods -n $NS -o json | jq -r '.items[].spec |
  [.volumes[]?.configMap.name, .volumes[]?.projected.sources[]?.configMap.name,
   .containers[].envFrom[]?.configMapRef.name, .containers[].env[]?.valueFrom.configMapKeyRef.name] | .[] | select(.)' | sort -u)
kubectl get cm -n $NS -o name | sed 's|configmap/||' | grep -vxF "$used" | grep -v kube-root-ca.crt
```
PVCs not mounted by any pod:
```bash
kubectl get pods -n $NS -o json | jq -r '.items[].spec.volumes[]?.persistentVolumeClaim.claimName' | sort -u > used
kubectl get pvc -n $NS -o name | sed 's|persistentvolumeclaim/||' | grep -vxFf used
```

## Before deleting
- Objects used by CronJobs or scaled-to-zero workloads have no pods right now; check
  CronJob and Deployment templates too.
- Secrets of type `kubernetes.io/service-account-token`, Helm release Secrets and
  cert-manager certificates are managed by controllers.
- The `kube-root-ca.crt` ConfigMap is used by projected service account volumes; leave it.
- With the `Delete` reclaim policy (the StorageClass default for dynamically provisioned
  volumes), deleting the PVC also deletes the PV and the backing storage. Snapshot first.

## Verify
Re-run kor; it lists nothing you meant to keep. Label objects you deliberately keep with
`kor/used=true` so kor ignores them (`kor/used=false` marks objects to always clean).

## Checked
2026-10-27 against the yonahd/kor README (main) and Kubernetes docs (kubernetes/website main,
v1.38 development tree; v1.37 is the latest release). Confirmed: kor subcommands (one kind per
subcommand, no comma lists), `-n/--include-namespaces`, `--exclude-namespaces`, `-o
table|json|yaml`, `--show-reason`, interactive `--delete`, the `kor/used` labels and what kor
checks per kind; the `kubernetes.io/service-account-token` Secret type; `kube-root-ca.crt` in
projected service account volumes; and the `Delete` reclaim policy behaviour and StorageClass
default. Fixed the `kor configmap,secret,pvc -A` example, which is not documented syntax.
Method: documentation only; no commands were run.
