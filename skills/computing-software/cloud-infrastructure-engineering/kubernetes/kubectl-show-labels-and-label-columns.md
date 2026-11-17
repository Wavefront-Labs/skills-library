---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-show-labels-and-label-columns
name: kubectl-show-labels-and-label-columns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, labels, show-labels, kubectl-label, label-selector, custom-columns]
level: practitioner
status: docs-checked
description: "View labels efficiently in kubectl: --show-labels, -L label columns, selector queries with -l, and finding objects missing a required label."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/", "https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/kubectl/pkg/cmd/get/humanreadable_flags.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Showing labels and label columns

```bash
kubectl get pods --show-labels                       # all labels in one column (noisy)
kubectl get pods -L app,version                      # selected labels as columns
kubectl get nodes -L topology.kubernetes.io/zone,node.kubernetes.io/instance-type
kubectl get pods -l app=web,tier!=cache              # equality
kubectl get pods -l 'env in (prod,staging),!canary'  # set-based; !key = key absent
kubectl get pods -l 'team'                           # has the key
```

## Find objects missing a label
```bash
kubectl get deploy -A -l '!team'
```

## Labels as data
```bash
kubectl get pods -o custom-columns=POD:.metadata.name,APP:.metadata.labels.app,HASH:.metadata.labels.pod-template-hash
```


## Gotchas
- Requirements in `-l` are comma-separated and all must match (logical AND); for an OR across different keys run two queries.
- Selectors on `kubectl delete -l` act on everything matching in the namespace; always run the
  same selector with `get` first.

## Checked
Checked 2026-10-24 against the kubectl get printer flags source (`--show-labels`, `-L`/`--label-columns`) and the Labels page (v1.37): equality-based `=`, `==`, `!=` and set-based `in`, `notin`, key-exists and `!key` selectors, comma acts as AND. Removed the jq and awk pipelines and the unconfirmed namespace-label and readability remarks.
Method: documentation only; no commands were run.
