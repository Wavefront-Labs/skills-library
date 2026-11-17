---
id: computing-software.ai-ml-engineering.kserve.kserve-inference-logger
name: kserve-inference-logger
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [logger, logger-mode, cloudevents, message-dumper, blob-storage-logger, logger-storage, orgkubeflowservinginferencerequest, json-format]
level: practitioner
status: docs-checked
description: "Log InferenceService requests and responses as CloudEvents with the logger field: mode, url sink (message dumper, S3 blob), and Knative Eventing payload logging variants."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/logger/index.md", "https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/logger/basic-logger.md", "https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/logger/blob-storage-logger.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inference logger

Logging is configured per component under `logger`. Variants in the docs: basic message dumper, request header metadata, TLS, Knative Eventing payload logger, and blob storage.

## Basic
Deploy a message dumper (a standard Kubernetes Deployment plus Service on port 80 -> 8080, or a Knative Service, image `event_display` from the Knative eventing-contrib releases), then:

```yaml
spec:
  predictor:
    model:
      modelFormat: {name: sklearn}
      storageUri: "gs://kserve-examples/models/sklearn/1.0/model"
    logger:
      mode: all
      url: http://message-dumper.default.svc.cluster.local
```

Each call emits CloudEvents of type `org.kubeflow.serving.inference.request` and `...response` (`specversion: 1.0`, JSON content). View with `kubectl logs` on the dumper pod (Knative: container `user-container`).

## Blob storage (S3 only)
The logger agent reads credentials from a ServiceAccount in the InferenceService namespace (Secret with `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, annotation `serving.kserve.io/s3-region`).

```yaml
    logger:
      mode: all
      url: s3://[YOUR_BUCKET_NAME]
      storage:
        path: /logs
        parameters: {type: s3, format: json}
        key: logger-credentials
        serviceAccountName: logger-sa
```

`format` must be `json` (`parquet` and `csv` are planned). Request and response are written as separate files; the response carries the prediction base64 encoded. Benefits listed: durable, scalable, decoupled from serving, analysable with big data tools. The Secret must be in the same namespace as the InferenceService.

## Checked
Confirmed against KServe's Inference Logger overview, Basic Inference Logger and Store Logs in Blob Storage pages: the five logger configurations, message dumper setup, the `mode: all` and `url` example, CloudEvent types and `specversion: 1.0`, log-viewing commands, S3-only blob storage, `json` as the only valid format, the credential Secret and ServiceAccount, request/response files with base64 predictions. The page's blob example is internally inconsistent (secret named `agent-logger-secret` but `key: logger-credentials`): check your own names.
Method: docs-only read of cited pages, 2026-11-08
