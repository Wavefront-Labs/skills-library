---
id: computing-software.ai-ml-engineering.ml-platform-engineering.scale-to-zero-model-inference
name: scale-to-zero-model-inference
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, scale-to-zero, serverless-inference, knative, keda, cold-start]
level: practitioner
status: draft
description: "Run inference that scales to zero when idle: KServe/Knative minReplicas 0, KEDA triggers, SageMaker serverless, async and inference-component options, and cold-start mitigation."
sources:
  - https://kserve.github.io/website/latest/modelserving/autoscaling/autoscaling/
  - https://keda.sh/docs/latest/concepts/scaling-deployments/
  - https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference-autoscale.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Scale-to-zero inference

**Goal:** rarely used models cost nothing while idle and still answer the first request within an acceptable delay.

## When it fits
Dev/staging endpoints, long-tail models, internal tools, batch-like async traffic. Not for strict real-time SLOs unless cold start is seconds and acceptable.

## Kubernetes
- **KServe (serverless mode on Knative):** `spec.predictor.minReplicas: 0`; Knative's activator buffers requests while a pod starts. Tune `autoscaling.knative.dev/scale-to-zero-pod-retention-period` to keep pods a while after the last request.
- **KEDA:** `ScaledObject` with `minReplicaCount: 0` and a trigger (Prometheus request rate, queue length in SQS/Kafka/Redis, HTTP add-on). Good for queue-driven workers.
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata: {name: embedder}
spec:
  scaleTargetRef: {name: embedder}
  minReplicaCount: 0
  maxReplicaCount: 10
  cooldownPeriod: 600
  triggers:
  - type: aws-sqs-queue
    metadata: {queueURL: https://sqs.us-east-1.amazonaws.com/123456789012/embed-jobs, queueLength: "20", awsRegion: us-east-1}
```
- GPU node pools must also scale to zero (cluster autoscaler / Karpenter) to save the real money; node startup adds minutes.

## Managed options
- **SageMaker Serverless Inference:** CPU only, memory 1-6 GB, max concurrency settings, provisioned concurrency to keep some warm; good for small models with intermittent traffic.
- **SageMaker Asynchronous Inference:** autoscaling `MinCapacity: 0`, requests queued in S3/SQS; scale on backlog per instance - supports GPUs and large payloads.
- **SageMaker inference components:** can scale copies to zero on shared endpoints.
- **Cloud Run (with GPUs where available)** and similar serverless container platforms scale to zero natively.

## Cold-start budget
Cold start = node provisioning (if scaled to zero) + image pull + model load + warm-up. Reduce each:
- slim images; pre-pulled or cached images on nodes; lazy image loading (e.g. SOCI/stargz);
- model weights on fast local or cached storage instead of downloading at start; safetensors for fast loading;
- warm-up request at startup so the first user does not pay JIT/compile cost.
Measure cold-start p95 and tell clients (async APIs or retries with longer timeouts).

## Verify
- [ ] Idle endpoint reaches zero pods (and zero GPU nodes) after the cooldown.
- [ ] Cold-start p95 measured and within the documented expectation.
