---
id: computing-software.cloud-infrastructure-engineering.kubernetes.quota-requires-requests-and-limits
name: quota-requires-requests-and-limits
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, resourcequota, quota-requires-limits, limitrange-defaults, quota-troubleshooting]
level: practitioner
status: docs-checked
description: "Why a compute ResourceQuota forces every pod to declare requests or limits, the resulting 'must specify' errors, and pairing quota with LimitRange defaults."
sources: ["https://kubernetes.io/docs/concepts/policy/resource-quotas/#requests-vs-limits", "https://kubernetes.io/docs/concepts/policy/limit-range/", "https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/", "https://kubernetes.io/docs/reference/using-api/api-concepts/#dry-run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quota that requires requests and limits

## Behaviour
If a namespace has a ResourceQuota tracking `requests.cpu`, `requests.memory`, `limits.cpu`
or `limits.memory`, every new pod must specify that value (requests or limits, to match the
quota keys), or creation is rejected with `403 Forbidden`:
```
Error creating: pods "web-7d9c-x" is forbidden: failed quota: compute:
must specify limits.cpu for: web; limits.memory for: web
```
For Deployments, the error appears only in ReplicaSet events; the Deployment just shows 0 ready.
```bash
kubectl describe rs -l app=web | sed -n '/Events/,$p'
```

## Fix with LimitRange defaults
```yaml
apiVersion: v1
kind: LimitRange
metadata: {name: defaults, namespace: team-a}
spec:
  limits:
  - type: Container
    defaultRequest: {cpu: 100m, memory: 128Mi}
    default:        {cpu: 500m, memory: 512Mi}     # becomes limits
```
The LimitRange admission controller applies these defaults before the quota check, so pods
without resources pass. In the kube-apiserver plugin order `LimitRanger` is listed before
`ResourceQuota`.

## Design choices
- Quota only `requests.*` if you do not want to force CPU limits (common: no CPU limits policy).
  Then only requests are mandatory.
- Use `limits.memory` in quota only if you also want every pod to set memory limits.
- Containers added by mutating webhooks (service mesh, secret agents) also count against the quota,
  so they need resources too unless a LimitRange supplies defaults.

## Verify
```bash
kubectl describe quota -n team-a
kubectl run t --image=nginx -n team-a --dry-run=server -o yaml | grep -A6 resources:   # defaults injected
```

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Pods must specify requests or limits for resources a quota tracks, otherwise admission rejects with 403 Forbidden:
  resource-quotas page. LimitRange applies defaults first, then the quota check: limit-range page.
- `failed quota: <name>: must specify <resources>` message: quota admission controller and pods evaluator source v1.37.1.
- `LimitRanger` is ordered before `ResourceQuota` in the kube-apiserver plugin list: `plugins.go` v1.37.1.
- `--dry-run=server` runs the admission chain: API concepts page (dry-run section).
- Removed: the claim that init containers are covered explicitly and the "must set resources" remark about sidecars, which the
  documentation does not state.

Method: documentation only; no commands were run.
