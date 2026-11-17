---
id: computing-software.ai-ml-engineering.mlops.endpoint-operational-metrics-cloudwatch-prometheus
name: endpoint-operational-metrics-cloudwatch-prometheus
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, endpoint-metrics, cloudwatch, prometheus, model-serving, alerting]
level: practitioner
status: draft
description: "Monitor model endpoint health: SageMaker CloudWatch invocation, latency and utilization metrics, Prometheus metrics from Triton/vLLM/KServe, dashboards and actionable alarms."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html
  - https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/metrics.html
  - https://docs.vllm.ai/en/latest/design/metrics.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Endpoint operational metrics

**Goal:** you know an endpoint is failing, slow or saturated before users do, and dashboards separate model time from platform time.

## SageMaker CloudWatch
Namespace `AWS/SageMaker`, dimensions `EndpointName`, `VariantName`:
- `Invocations`, `InvocationsPerInstance` - traffic.
- `Invocation4XXErrors`, `Invocation5XXErrors` - client vs server errors.
- `ModelLatency` (microseconds, time in your container) and `OverheadLatency` (SageMaker overhead).
- `ModelSetupTime` - serverless cold starts.
Namespace `/aws/sagemaker/Endpoints`: `CPUUtilization`, `MemoryUtilization`, `GPUUtilization`, `GPUMemoryUtilization`, `DiskUtilization` (percent summed across cores/GPUs - 400% on a 4-GPU instance is full).
```bash
aws cloudwatch put-metric-alarm --alarm-name churn-5xx --namespace AWS/SageMaker \
  --metric-name Invocation5XXErrors --dimensions Name=EndpointName,Value=churn Name=VariantName,Value=primary \
  --statistic Sum --period 60 --evaluation-periods 5 --datapoints-to-alarm 3 --threshold 5 \
  --comparison-operator GreaterThanThreshold --alarm-actions $SNS_TOPIC
```
Prefer error-rate alarms (metric math 5XX / Invocations) over raw counts for variable traffic.

## Prometheus (self-hosted servers)
- **Triton** `:8002/metrics`: `nv_inference_request_success`, `nv_inference_request_failure`, `nv_inference_queue_duration_us`, `nv_inference_compute_infer_duration_us`, `nv_gpu_utilization`.
- **vLLM** `/metrics`: `vllm:time_to_first_token_seconds`, `vllm:e2e_request_latency_seconds`, `vllm:num_requests_running`, `vllm:num_requests_waiting`, KV cache usage gauge.
- **KServe/Knative**: request count and latency per revision.
```
histogram_quantile(0.95, sum by (le, model) (rate(vllm:e2e_request_latency_seconds_bucket[5m])))
```

## Dashboard (per endpoint)
Traffic, error rate (4xx and 5xx separately), p50/p95/p99 latency split into model vs overhead or queue vs compute, utilization (CPU/GPU/memory), instance count vs autoscaling max, and deploy markers.

## Alerts that matter
- 5xx error rate > 1% for 5 minutes.
- p95 latency above SLO for 10 minutes.
- Queue time rising while compute time flat = under-provisioned.
- Instance count at max for 15 minutes.
- Zero invocations during expected traffic hours (broken upstream).
Each alert links a runbook: scale, roll back, or check upstream.

## Verify
- [ ] Synthetic 5xx injection triggers the alarm.
- [ ] Dashboards show per-variant metrics so canaries are comparable.
