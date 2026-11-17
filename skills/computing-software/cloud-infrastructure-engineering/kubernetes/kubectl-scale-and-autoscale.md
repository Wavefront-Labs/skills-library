---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-scale-and-autoscale
name: kubectl-scale-and-autoscale
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl-scale, kubectl-autoscale, scale-subresource, hpa, ckad, cka]
level: practitioner
status: docs-checked
description: "Scale workloads with kubectl scale (preconditions, selectors, StatefulSets, to zero) and create HPAs with kubectl autoscale without fighting GitOps or an HPA."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_scale/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_autoscale/", "https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/kubectl/pkg/cmd/autoscale/autoscale.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl scale and kubectl autoscale

## kubectl scale
```bash
kubectl scale deploy/web --replicas=5
kubectl scale deploy/web --current-replicas=3 --replicas=5     # only if currently 3 (safe in scripts)
kubectl scale deploy -l tier=batch --replicas=0 -n jobs          # by selector
kubectl scale sts/db --replicas=3                                 # ordinals added/removed from the top
kubectl scale --replicas=0 deploy --all -n staging                # park a namespace overnight
kubectl scale rs/web-7c9d --replicas=0                            # works but the Deployment fights back
```
The `kubectl scale` reference covers Deployments, ReplicaSets, ReplicationControllers and
StatefulSets. `--current-replicas` and `--resource-version` are preconditions; `--timeout`
waits for the scale operation.

## kubectl autoscale
```bash
kubectl autoscale deploy web --min=2 --max=10 --cpu=70%
kubectl get hpa web -w
```
Tries the `autoscaling/v2` API first and falls back to `autoscaling/v1`. `--cpu` and `--memory`
each take a percentage (average utilization of requests) or a quantity (average value, e.g.
`500m`, `200Mi`); `--cpu-percent` is deprecated and cannot be combined with `--cpu`. `--max` is
required. Needs metrics-server and `resources.requests.cpu` on the containers (for percentage
targets) or TARGETS shows `<unknown>`. For custom metrics or `behavior`, write the HPA YAML
(`kubectl autoscale ... --dry-run=client -o yaml` as a starting point).

## Who owns `.spec.replicas`
- With an HPA attached, the HPA controller re-evaluates every sync period (default 15s) and sets
  `replicas` again, so a manual `kubectl scale` does not stick. To pin, edit the HPA
  `minReplicas` or delete it.
- Any GitOps tool that applies a manifest containing `replicas:` fights the HPA the same way.
  The HPA docs recommend removing `spec.replicas` from the manifest when an HPA owns it
  (use `kubectl apply edit-last-applied`, or the Server-Side Apply ownership transfer, to avoid
  a one-time drop to the default of 1).
- `kubectl apply` of a manifest with `replicas: 3` scales an HPA-managed Deployment to 3, which
  the HPA docs describe as thrashing or flapping. Omit `replicas` from templates.

## Gotchas
- Scaling a StatefulSet down does not delete PVCs unless
  `persistentVolumeClaimRetentionPolicy.whenScaled: Delete` is set (the default is `Retain`).

## Verify
- [ ] `kubectl get deploy web -o jsonpath='{.spec.replicas} {.status.readyReplicas}'` matches the intent.
- [ ] Exactly one actor (HPA, GitOps, or human) owns replicas per workload.

## Checked

Checked 2026-10-24 against the kubectl source (staging/src/k8s.io/kubectl/pkg/cmd/autoscale/autoscale.go and scale/scale.go on master) and Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24).
- `--cpu` and `--memory` accept percentages or quantities; `--cpu-percent` is deprecated and mutually exclusive with `--cpu`; v2 first, v1 fallback.
- `kubectl scale` flags `--replicas`, `--current-replicas`, `--all`, `--resource-version`, `--timeout`, and the supported kinds in its help text.
- StatefulSet `persistentVolumeClaimRetentionPolicy.whenScaled` (retention policy feature stable from 1.32): feature gate StatefulSetAutoDeletePVC.

Method: documentation only; no commands were run.
