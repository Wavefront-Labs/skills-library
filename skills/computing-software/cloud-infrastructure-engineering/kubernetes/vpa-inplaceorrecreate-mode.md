---
id: computing-software.cloud-infrastructure-engineering.kubernetes.vpa-inplaceorrecreate-mode
name: vpa-inplaceorrecreate-mode
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, vpa, inplaceorrecreate, in-place-resize, inplacepodverticalscaling]
level: practitioner
status: docs-checked
description: "Use VPA updateMode InPlaceOrRecreate to resize pod resources without eviction where possible, its prerequisites, fallback behaviour and limits."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/features.md#in-place-updates-inplaceorrecreate", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/flags.md", "https://kubernetes.io/docs/tasks/configure-pod-container/resize-container-resources/", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPA InPlaceOrRecreate

## What it is
A VPA update mode that applies new requests through the pod `resize` subresource (in-place pod
resize) instead of evicting. If an in-place resize is infeasible or stays pending too long, the
updater falls back to eviction as in `Recreate`.

## Prerequisites
- Kubernetes 1.33 or later with `InPlacePodVerticalScaling` enabled (beta and on by default
  from 1.33, stable from 1.35).
- VPA 1.4.0 or later. The mode was alpha in VPA 1.4.0 (needed the `InPlaceOrRecreate`
  feature gate), beta and on by default from 1.5.0, and the gate was removed in 1.7.0.

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata: {name: api}
spec:
  targetRef: {apiVersion: apps/v1, kind: Deployment, name: api}
  updatePolicy:
    updateMode: InPlaceOrRecreate
  resourcePolicy:
    containerPolicies:
    - containerName: '*'
      minAllowed: {cpu: 100m, memory: 128Mi}
      maxAllowed: {cpu: "2", memory: 2Gi}
```

## Behaviour details
- VPA first tries the in-place update and falls back to recreation when the resize is
  infeasible, deferred for more than 5 minutes, in progress for more than 1 hour, would change
  the pod's QoS class, or needs a memory limit decrease that VPA cannot apply in place.
- Updates are attempted when requests are outside the recommended bounds, after a quick OOM,
  and, for pods running longer than 12 hours, when recommendations differ by more than 10%.
- All containers in a pod are updated together; disruption cannot be ruled out because the
  container runtime performs the resize.
- `--in-place-skip-disruption-budget` (default false, beta) skips disruption budget checks for
  in-place updates when every container has a `NotRequired` resize policy or none.

## Verify
```bash
kubectl get pod <p> -o jsonpath='{.spec.containers[0].resources}{"\n"}{.status.containerStatuses[0].resources}{"\n"}'
kubectl get pod <p> -o jsonpath='{.status.conditions[?(@.type=="PodResizePending")]}'
kubectl get events --field-selector reason=InPlaceResizedByVPA
```
Restart count unchanged with new resources = in-place worked.
Updater metrics: `vpa_updater_in_place_updated_pods_total` and `vpa_updater_failed_in_place_update_attempts_total`.

## Checked

Checked 2026-10-24 against the kubernetes/autoscaler vertical-pod-autoscaler docs (features.md and flags.md on master, VPA 1.8.1) and Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24).
- Mode name, stages (alpha 1.4.0, beta 1.5.0, gate removed 1.7.0), Kubernetes 1.33+ requirement, fallback conditions, 12 h and 10% rule and monitoring metrics: features.md.
- `--in-place-skip-disruption-budget` default false and its condition: flags.md.
- `InPlacePodVerticalScaling` stages (beta 1.33, stable 1.35): feature gate source in kubernetes/website. The Kubernetes resize page confirms `resizePolicy` values `NotRequired` (default) and `RestartContainer`, the `PodResizePending` condition with reasons `Infeasible` and `Deferred`, and that the QoS class cannot change in a resize.
- `EvictedByVPA` and `InPlaceResizedByVPA` event reasons exist in the VPA updater source.

Method: documentation only; no commands were run.
