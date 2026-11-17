---
id: computing-software.ai-ml-engineering.seldon-core-2.drift-and-outlier-detectors
name: drift-and-outlier-detectors
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, drift-detection, outlier-detection, alibi-detect, batch, async-pipeline-branch, kafka-alerts]
level: advanced
status: docs-checked
description: "Deploy Alibi-Detect drift and outlier detectors as Models with the alibi-detect requirement, run drift off the synchronous path with batch size, and read alerts from Kafka."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/drift.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Drift and outlier detection

Detectors are ordinary Models. Run any saved Alibi-Detect drift or outlier model on MLServer by adding the requirement `alibi-detect`.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Model
metadata:
  name: cifar10-drift
spec:
  storageUri: "gs://seldon-models/scv2/examples/mlserver_1.3.5/cifar10/drift-detector"
  requirements:
    - mlserver
    - alibi-detect
```

## In a pipeline
Drift detectors normally sit on an asynchronous branch that is not connected to the pipeline output. Batch the inputs to a drift step with `batch.size`:

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Pipeline
metadata:
  name: cifar10-production
spec:
  steps:
    - name: cifar10
    - name: cifar10-outlier
    - name: cifar10-drift
      batch:
        size: 20
  output:
    steps:
    - cifar10
    - cifar10-outlier.outputs.is_outlier
```

The outlier result `is_outlier` is returned synchronously. Drift alerts are read from the Kafka topic of the drift model.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/drift.md (read in full). Dropped an unsupported sentence on how outlier detectors are defined; the page example shows an outlier step in the pipeline only.
