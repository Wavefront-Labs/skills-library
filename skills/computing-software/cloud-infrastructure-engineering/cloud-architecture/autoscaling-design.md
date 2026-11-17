---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.autoscaling-design
name: autoscaling-design
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, scalability, autoscaling-design, target-tracking, step-scaling, scheduled-scaling, predictive-scaling, hpa, keda, scale-in-protection, cooldown]
level: practitioner
status: docs-checked
description: "Design autoscaling that keeps up without flapping: choosing the scaling metric, target tracking vs step vs scheduled/predictive, min/max bounds, warm-up and stabilisation."
sources: ["https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-target-tracking.html", "https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/", "https://learn.microsoft.com/azure/architecture/best-practices/auto-scaling"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoscaling policy design

## Choose the metric
Scale on the metric that saturates first and tracks load linearly:
- Request-driven web/API: requests per target (EC2 Auto Scaling `ALBRequestCountPerTarget`, which needs the `ResourceLabel` parameter), or CPU if CPU-bound.
- Queue workers: queue length or event-source metrics (Azure Container Apps scales with KEDA on event sources).
- Memory: HPA can scale on memory, but choose it deliberately and test that adding replicas actually lowers it.

## Policy types
- **Target tracking**: keep a metric at a target value; scales in more gradually than it scales out, prioritising availability.
- **Step scaling**: more control than target tracking; bigger jumps for bigger breaches.
- **Scheduled**: provision ahead of predictable demand, e.g. known daily or weekly patterns.
- **Predictive** (Azure Virtual Machine Scale Sets predictive autoscale): start in forecast-only mode and compare with actual usage; it can scale out as early as one hour before predicted demand. Keep metric-based rules for unexpected demand and scale-in.

## Settings
1. **Min** sized for baseline plus failure of a zone; **max** sized to protect downstreams and budget.
2. **Warm-up / readiness**: set an EC2 Auto Scaling instance warmup so booting instances are not counted in group metrics; Azure Monitor rules take a per-rule cooldown.
3. **Scale out fast, scale in slow**: HPA defaults are no scale-up stabilisation and a 300-second scale-down stabilisation window (`behavior.scaleDown.stabilizationWindowSeconds`).
4. Start with extra capacity headroom and tune the rules against the observed load.
5. If response targets do not allow requests to wait for scaling, provision ahead of predictable demand and keep headroom for unpredictable demand.

## Gotchas
- Target too high leaves no headroom while new capacity boots.
- Scaling on a metric your scaling changes non-linearly (latency) → oscillation.
- Downstream DB can't scale with the stateless tier — cap max or add pooling.

## Verify
- [ ] Load test ramp: latency SLO held while scaling; no flapping in scale events.
- [ ] Max limits documented with the reason.

## Checked
2026-11-08. Confirmed against the three cited pages: ALBRequestCountPerTarget and ResourceLabel, instance warmup, gradual scale-in of target tracking, HPA default 300-second scale-down window and no scale-up window, Azure predictive autoscale (forecast-only mode, one hour ahead), per-rule cooldown, headroom advice, KEDA in Container Apps. Removed: CPU 50-60% figure, AWS predictive scaling, scale-in protection and lifecycle hooks, Cluster Autoscaler/Karpenter and memory claims not on the cited pages.
Method: documentation only; no commands were run.
