---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-label-annotate-and-field-selectors
name: kubectl-label-annotate-and-field-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl-label, kubectl-annotate, field-selector, label-columns, cka, ckad]
level: practitioner
status: docs-checked
description: "Add, change and remove labels and annotations with kubectl (overwrite, bulk, resourceVersion), show them as columns, and filter server-side with field selectors."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_label/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_annotate/", "https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/label", "https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl label, annotate and field selectors

## Labels
```bash
kubectl label pod web-1 tier=frontend
kubectl label pod web-1 tier=edge --overwrite        # required to change an existing value
kubectl label pod web-1 tier-                        # remove (trailing dash)
kubectl label pods -l app=web canary=true            # bulk by selector
kubectl label pods --all -n staging env=staging
kubectl label node worker-3 disktype=ssd
kubectl label ns team-a pod-security.kubernetes.io/enforce=baseline --dry-run=server
kubectl label pod web-1 x=y --resource-version=12345   # fails if the object changed (optimistic lock)
kubectl get pods -L app,tier                          # labels as columns
kubectl get pods --show-labels
```
Labelling pods managed by a controller is temporary — the next rollout recreates them from the
template. Change the template for durable labels. Changing a pod's labels removes it from its ReplicaSet and a replacement starts, which is useful for debugging.

## Annotations
```bash
kubectl annotate deploy web kubernetes.io/change-cause="bump to 1.8.3"
kubectl annotate deploy web owner=team-a --overwrite
kubectl annotate deploy web owner-
kubectl annotate pods -l app=web prometheus.io/scrape=true
```
Annotations are not used to identify and select objects.

## Field selectors (server-side filter on fields)
```bash
kubectl get pods -A --field-selector status.phase=Failed
kubectl get pods -A --field-selector spec.nodeName=worker-3
kubectl get pods --field-selector status.phase!=Running,status.phase!=Succeeded
kubectl get events -A --field-selector type=Warning,reason=FailedScheduling
kubectl get events --field-selector involvedObject.name=web-1
kubectl get secrets --field-selector type=kubernetes.io/tls
kubectl get ns --field-selector status.phase=Terminating
kubectl delete pods -A --field-selector status.phase=Succeeded
```
Supported fields are limited per resource (all support `metadata.name`, `metadata.namespace`;
pods: `spec.nodeName`, `spec.restartPolicy`, `spec.schedulerName`, `spec.serviceAccountName`, `spec.hostNetwork`,
`status.phase`, `status.podIP`, `status.podIPs`, `status.nominatedNodeName`). An unsupported field returns a BadRequest
(`... is not a known field selector`). Operators: `=`, `==`, `!=`; comma = AND. CRDs support only name/
namespace unless they declare `selectableFields` (beta and on by default in 1.31, stable in 1.32).

## Verify
- [ ] `kubectl get pods -L <key>` shows the intended values; field-selector queries return expected sets.

## Checked
Checked 2026-10-24 against the kubectl label source (main), the field selector, label, annotation and ReplicaSet pages (v1.37) and the feature-gate list: `--overwrite`, `--resource-version` (single resource only), `--all`, `-l`, trailing `-` removal, supported field list, `=`/`==`/`!=` operators with comma as AND, the unsupported-field error text, `CustomResourceFieldSelectors` stages (beta 1.31, stable 1.32), removing a pod from a ReplicaSet by changing labels. The `kubectl annotate` flags mirror `label`.
Method: documentation only; no commands were run.
