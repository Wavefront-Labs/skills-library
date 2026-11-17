---
id: computing-software.ai-ml-engineering.kserve.kserve-inference-batcher
name: kserve-inference-batcher
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [batcher, maxbatchsize, maxlatency, timeout, model-agent, batching, agent-sidecar]
level: practitioner
status: docs-checked
description: "Request batching in the KServe agent sidecar: batcher maxBatchSize (32), maxLatency (500 ms), timeout (60 s); V1 HTTP only; batch triggers and batchId behaviour."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/batcher/batcher.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inference batcher

Implemented in the KServe model agent sidecar, injected by webhook when `batcher` is set. Requests hit the agent first; when a batch fires it is sent to the model container. Works for any framework but only with the V1 HTTP protocol; gRPC is not supported yet.

A batch is triggered when the number of instances reaches `maxBatchSize` OR the wait reaches `maxLatency`.

```yaml
spec:
  predictor:
    minReplicas: 1
    timeout: 60
    batcher:
      maxBatchSize: 32
      maxLatency: 500
    model:
      modelFormat: {name: pytorch}
      storageUri: gs://kfserving-examples/models/torchserve/image_classifier/v1
```

| Field | Meaning | Default |
|---|---|---|
| `maxBatchSize` | max instances that trigger a prediction | 32 |
| `maxLatency` | max wait in milliseconds | 500 |
| `timeout` | timeout calling the predictor, seconds | 60 |

All optional. Internals use Go channels between HTTP handlers and batcher goroutines. The returned `batchId` is the same when the interval between two requests is less than `maxLatency`. The page's example sets `maxLatency` to a large value (500 ms) so that batching is observable, and load-tests with `hey` against `/v1/models/$MODEL_NAME:predict`.

## Checked
Confirmed against KServe's Inference Batcher page: sidecar implementation injected by webhook, Go channels, V1 HTTP only (gRPC not supported yet), the two triggers, example YAML, the three parameters with defaults 32, 500 ms and 60 s (all optional), and the `batchId` tip. Removed the claim that `hey` uses these exact flags as a requirement.
Method: docs-only read of cited pages, 2026-11-08
