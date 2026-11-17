---
id: computing-software.ai-ml-engineering.mlops.endpoint-autoscaling-policies
name: endpoint-autoscaling-policies
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, endpoint-autoscaling, sagemaker, target-tracking, kserve, load-testing]
level: practitioner
status: gated
description: "Set autoscaling for model endpoints: SageMaker target tracking on invocations or concurrency, Vertex replica targets, KServe/Knative concurrency, cooldowns and load-test sizing."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/endpoint-auto-scaling.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/endpoint-scaling-loadtest.html
  - https://cloud.google.com/vertex-ai/docs/general/deployment#scaling
  - https://kserve.github.io/website/latest/modelserving/autoscaling/autoscaling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Endpoint autoscaling policies

**Goal:** endpoints add capacity before latency degrades and shed it when idle, without flapping.

## Size from a load test first
Find the maximum sustainable requests per second per instance at your latency SLO (ramp load until p95 breaches). Target 50-70% of that per instance so there is headroom while new instances start.

## SageMaker
```python
aas = boto3.client("application-autoscaling")
rid = "endpoint/churn/variant/primary"
aas.register_scalable_target(ServiceNamespace="sagemaker", ResourceId=rid,
    ScalableDimension="sagemaker:variant:DesiredInstanceCount", MinCapacity=2, MaxCapacity=20)
aas.put_scaling_policy(PolicyName="invocations-target", ServiceNamespace="sagemaker", ResourceId=rid,
    ScalableDimension="sagemaker:variant:DesiredInstanceCount", PolicyType="TargetTrackingScaling",
    TargetTrackingScalingPolicyConfiguration={
        "TargetValue": 600.0,     # invocations per instance per MINUTE = 0.6 * max_rps * 60
        "PredefinedMetricSpecification": {"PredefinedMetricType": "SageMakerVariantInvocationsPerInstance"},
        "ScaleOutCooldown": 60, "ScaleInCooldown": 600})
```
- The invocations metric is per minute, so scaling reacts in minutes; for spiky or long-running (LLM) requests use the high-resolution concurrency metric (`SageMakerVariantConcurrentRequestsPerModelHighResolution` / inference-component concurrency) where available. (gated: unconfirmed, source is paywalled or blocked)
- Add scheduled scaling for known daily peaks; step scaling on a custom metric for queue-driven async endpoints (scale on `ApproximateBacklogSizePerInstance`, min 0 for async).
- Inference components support scale to zero; real-time variants keep `MinCapacity >= 1`.

## Vertex AI
`min_replica_count`, `max_replica_count`, and `autoscaling_target_cpu_utilization` (default 60) or `autoscaling_target_accelerator_duty_cycle` for GPU. Scale-out evaluates over minutes; keep min replicas high enough for the first burst.

## KServe / Knative
```yaml
metadata:
  annotations:
    autoscaling.knative.dev/target: "4"         # concurrent requests per pod
    autoscaling.knative.dev/min-scale: "1"
    autoscaling.knative.dev/max-scale: "10"
```
Concurrency-based scaling suits model servers better than CPU. For GPU pods, set targets from measured batch capacity; use KEDA on queue depth or custom metrics (tokens/s) for LLM servers.

## Pitfalls
- Scale-in cooldown too short: flapping, cold starts, and dropped in-flight requests.
- Max capacity hits account quotas or GPU availability; check quotas and alert at 80% of max.
- Slow model load (large weights) makes reactive scaling useless; pre-scale or keep warm minimums.
- CPU utilization is a poor signal for GPU-bound or I/O-bound servers.

## Verify
- [ ] Load test with a step increase shows scale-out before p95 breaches the SLO.
- [ ] Scale-in after load drop without errors.
- [ ] Alarms on max-capacity reached and on throttling.

## Checked

2026-11-02

- Confirmed: SageMaker endpoint auto scaling and load-test pages, and the Vertex AI deployment scaling page, were fetched (stubs/overviews).
- Removed or gated: The KServe autoscaling page returned no text and the fetched pages do not list API parameter names, predefined metric names or the numeric targets used here; gated, confirm in the Application Auto Scaling and Vertex AI references. Percentage targets are not documented defaults.

Method: documentation only; no commands were run.
