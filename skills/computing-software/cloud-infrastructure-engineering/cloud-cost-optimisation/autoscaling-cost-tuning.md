---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.autoscaling-cost-tuning
name: autoscaling-cost-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-optimization, autoscaling-cost-tuning, autoscaling, hpa, karpenter, cluster-autoscaler, predictive-scaling, scheduled-scaling]
level: advanced
status: docs-checked
description: "Tune autoscaling for cost: higher target utilisation, scale-in speed, sensible minimums, scheduled and predictive scaling, HPA behaviour, and node consolidation."
sources: ["https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-target-tracking.html", "https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/", "https://karpenter.sh/docs/concepts/disruption/", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoscaling tuning for cost

Autoscaling saves money only if it actually scales in. Default settings are conservative: low
target utilisation, slow scale-in, high minimums.

## Levers
1. **Target utilisation**: a higher target tracking value means a smaller fleet. Validate latency
   under load first.
2. **Scale-in speed**: shorter stabilisation windows release capacity faster; keep scale-out fast
   and scale-in moderate to avoid flapping.
3. **Minimums**: min capacity sized for the off-peak floor, not the daily peak; per-AZ minimums only
   where resilience needs them.
4. **Scheduled scaling**: known patterns (business hours, batch windows) and non-prod to zero at
   night.
5. **Right metric**: scale on a metric that tracks load (requests, queue depth) rather than CPU
   where CPU does not.

## Kubernetes
```yaml
# HPA: faster scale-down than the 300 s default, still damped
behavior:
  scaleDown:
    stabilizationWindowSeconds: 120
    policies: [{type: Percent, value: 50, periodSeconds: 60}]
```
- Pods: accurate requests (VPA recommendations) so HPA utilisation and bin-packing are meaningful.
- Nodes: **Karpenter** `disruption.consolidationPolicy: WhenEmptyOrUnderutilized` with
  `consolidateAfter`, diverse instance types and spot; or Cluster Autoscaler
  `--scale-down-utilization-threshold` and `--scale-down-unneeded-time` (check the FAQ for defaults).
- PodDisruptionBudgets that allow eviction; `cluster-autoscaler.kubernetes.io/safe-to-evict`
  annotations for pods that block scale-down.

## Steps
1. Plot capacity vs demand per service for a week; the gap is the opportunity.
2. Change one parameter at a time; watch latency, error rate and scaling events.
3. Re-check commitments: a smaller, spikier fleet changes the commitment floor.

## Gotchas
- Scale-in that is too aggressive causes oscillation and cold starts; watch scaling activity counts.
- Long connection draining or JVM warm-up needs slower scale-in.
- Blocking PDBs or local-storage pods can stop node scale-down (see the Cluster Autoscaler FAQ).

## Verify
- [ ] Average utilisation of autoscaled fleets increased without SLO breaches.
- [ ] Off-peak capacity tracks demand within the agreed headroom.

## Checked
2026-11-01. Confirmed in the Kubernetes HPA page (stabilizationWindowSeconds, 300-second default scale-down window,
Percent policies), Karpenter disruption page (consolidationPolicy WhenEmptyOrUnderutilized, consolidateAfter), the
Cluster Autoscaler FAQ (scale-down flags, safe-to-evict) and the EC2 target tracking page. Removed: the 40% to 60-70%
fleet-size claim, predictive scaling for EC2 and VMSS, warm pools, and the example flag values.
Method: documentation only; no commands were run.
