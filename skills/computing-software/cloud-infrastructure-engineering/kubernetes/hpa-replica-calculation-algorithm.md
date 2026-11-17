---
id: computing-software.cloud-infrastructure-engineering.kubernetes.hpa-replica-calculation-algorithm
name: hpa-replica-calculation-algorithm
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, hpa, hpa-algorithm, hpa-tolerance, target-utilization, stabilizationwindowseconds]
level: practitioner
status: docs-checked
description: "The HPA replica formula, 10 percent tolerance, how not-ready and missing-metric pods are treated, and why HPA seems to scale late or not at all."
sources: ["https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/#algorithm-details", "https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/#tolerance", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HPA replica calculation

## Formula
`desiredReplicas = ceil(currentReplicas * currentMetricValue / desiredMetricValue)`

For `averageUtilization: 60` with pods at 90% CPU of their requests and 4 replicas:
`ceil(4 * 90/60) = 6`. Utilisation is relative to **requests**, so pods without CPU requests
cannot be scaled on CPU utilisation.

## Tolerance
If `|current/desired - 1| <= 0.1` (controller-manager `--horizontal-pod-autoscaler-tolerance`,
default 0.1) nothing happens. With target 60%, usage between 54% and 66% causes no change.
A per-HPA tolerance can be set in `behavior.scaleUp.tolerance` and `behavior.scaleDown.tolerance`
(feature gate HPAConfigurableTolerance: alpha 1.33, beta 1.35 and off by default, stable and
on by default from 1.37). Without it the cluster-wide default applies.

## Not-ready and missing metrics
- For per-pod resource metrics, pods with a deletion timestamp are ignored and failed pods are discarded.
- When scaling on CPU, a pod that is not yet ready, or whose latest metric point predates becoming
  ready, is set aside. `--horizontal-pod-autoscaler-initial-readiness-delay` (default 30 s) and
  `--horizontal-pod-autoscaler-cpu-initialization-period` (default 5 min) define how "first ready"
  is judged.
- Pods with missing metrics are assumed to use 100% of the desired value on scale-down and 0% on
  scale-up. If the workload would scale up, not-yet-ready pods are also assumed to use 0%.
- After this adjustment the ratio is recomputed; if it reverses the scale direction or falls
  within tolerance, no scaling happens.
These make the HPA conservative: it scales up less than the raw numbers suggest during rollouts.

## Multiple metrics
Each metric yields a desired count; the HPA takes the max.

## Timing
- Controller sync every 15 s (`--horizontal-pod-autoscaler-sync-period`).
- Scale-down stabilisation window default 300 s (`--horizontal-pod-autoscaler-downscale-stabilization`,
  default 5 minutes): the HPA uses the highest recommendation in the window. Scale-up
  `stabilizationWindowSeconds` defaults to 0.
- The metrics pipeline adds its own lag on top of the sync period.

## Debug
```bash
kubectl describe hpa web          # Metrics: current/target, Conditions: AbleToScale, ScalingActive, ScalingLimited
kubectl get hpa web -o jsonpath='{.status}'
```
`ScalingLimited True TooManyReplicas` means maxReplicas is the cap, not the algorithm.

## Checked

Checked 2026-10-24 against Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24).
- Formula, 0.1 default tolerance, missing-metric 100%/0% rule, not-yet-ready 0% rule, direction-reversal rule, 30 s and 5 min readiness flags, 15 s sync period and 5 minute downscale stabilization: HPA page.
- HPAConfigurableTolerance stages (alpha 1.33, beta 1.35 off by default, stable 1.37 on and locked): feature gate source in kubernetes/website.
- Condition reasons `TooManyReplicas` and `TooFewReplicas` exist in the controller source.

Method: documentation only; no commands were run.
