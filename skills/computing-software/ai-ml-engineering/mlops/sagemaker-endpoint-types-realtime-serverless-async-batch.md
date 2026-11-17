---
id: computing-software.ai-ml-engineering.mlops.sagemaker-endpoint-types-realtime-serverless-async-batch
name: sagemaker-endpoint-types-realtime-serverless-async-batch
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-deployment, async-inference, serverless-inference, batch-transform, sagemaker-endpoints, real-time-inference]
level: practitioner
status: docs-checked
description: "Choose between SageMaker real-time, serverless, asynchronous inference and batch transform by payload, latency, traffic and GPU needs, with config essentials."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SageMaker endpoint types

**Goal:** pick the inference option that fits latency, payload and traffic shape, instead of defaulting to an always-on instance.

## Decision table
| Need | Option |
|---|---|
| Low latency, steady traffic, GPUs | Real-time endpoint (instance-based) |
| Spiky/low traffic, small CPU models, tolerate cold starts | Serverless inference |
| Large payloads or long processing (seconds to minutes), queue OK | Asynchronous inference |
| Score a whole dataset, no endpoint needed | Batch transform |

## Real-time
- Check the SageMaker quotas page for payload and invocation-timeout limits. Autoscale with Application Auto Scaling target tracking (load-test to find the per-instance target).
- Use production variants for A/B traffic splits.

## Serverless
```python
from sagemaker.serverless import ServerlessInferenceConfig
predictor = model.deploy(serverless_inference_config=ServerlessInferenceConfig(memory_size_in_mb=4096, max_concurrency=10))
```
- Memory 1024-6144 MB; max concurrency per endpoint up to 200; no GPUs. Check the quotas page for payload and timeout limits.
- Cold starts of seconds after idle; provisioned concurrency removes them at a cost.
- Container image size and model load time dominate cold start: keep images slim, load lazily only what's needed.

## Asynchronous
```python
from sagemaker.async_inference import AsyncInferenceConfig
predictor = model.deploy(instance_type="ml.g5.xlarge", initial_instance_count=1,
    async_inference_config=AsyncInferenceConfig(output_path="s3://bucket/async-out/",
        notification_config={"SuccessTopic": sns_ok, "ErrorTopic": sns_err}))
resp = predictor.predict_async(input_path="s3://bucket/in/req1.json")
```
- Payloads up to 1 GB via S3, processing up to 1 hour, internal queue.
- Can **scale to zero**: autoscaling policy with min capacity 0 plus a backlog-based scaling policy to wake up (see the async inference autoscaling docs for the metric).
- Good fit for document/video processing and large LLM batch jobs with variable load.

## Batch transform
```python
t = model.transformer(instance_count=4, instance_type="ml.m5.xlarge", strategy="MultiRecord",
                      max_payload=6, assemble_with="Line", output_path="s3://bucket/preds/")
t.transform("s3://bucket/to-score/", content_type="text/csv", split_type="Line",
            input_filter="$[1:]", join_source="Input", output_filter="$[0,-1]")
```
- `split_type="Line"` + `MultiRecord` batches lines into requests up to `max_payload` MB (the maximum is 100 MB).
- `input_filter`/`join_source`/`output_filter` drop the ID column for the model and rejoin it to predictions.
- The number of output files equals the number of input files; split very large inputs so the work can spread across instances.

## Verify
- [ ] Payload size and p99 processing time checked against the option's limits.
- [ ] Autoscaling (or scale-to-zero) policy tested with a load burst.
- [ ] Cost per 1k predictions compared across the candidate options.

## Checked

2026-11-02. Checked against the SageMaker Developer Guide pages for deploy-model, serverless-endpoints, async-inference and batch-transform. Confirmed: serverless memory 1024-6144 MB, max concurrency per endpoint up to 200, no GPU support, cold starts, provisioned concurrency; async payloads up to 1 GB, processing up to one hour, scale to zero; batch transform MaxPayloadInMB must not exceed 100 MB, SplitType Line, BatchStrategy. Removed because the fetched pages do not state them: real-time 6 MB and 60 s limits, serverless 4 MB and 60 s limits, vCPU-scales-with-memory, the SageMakerVariantInvocationsPerInstance and HasBacklogWithoutCapacity metric names, and the minimum-two-instances advice.

Method: documentation only; no commands were run.
