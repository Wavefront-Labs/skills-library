---
id: computing-software.ai-ml-engineering.seldon-core-2.partial-scheduling-minreplicas
name: partial-scheduling-minreplicas
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, partial-scheduling, minreplicas, modelavailable, replicas, scheduling]
level: advanced
status: docs-checked
description: "Partial scheduling from Seldon Core 2.9: set minReplicas so a Model serves with fewer replicas than desired, and read READY, DESIRED and AVAILABLE REPLICAS to classify state."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/models/scheduling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Partial scheduling with minReplicas

From Core 2 version 2.9 the Scheduler can partially schedule a Model: it loads enough replicas to reach `spec.minReplicas`, up to the number of Server replicas currently available. This gives flexibility to serve traffic while optimising provisioning.

## Enabling
Define `spec.minReplicas` on the Model. It tells Core 2 the minimum replica count needed for serving.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Model
metadata:
  name: iris
spec:
  storageUri: "gs://seldon-models/scv2/samples/mlserver_1.5.0/iris-sklearn"
  requirements:
  - sklearn
  replicas: 3
  minReplicas: 1
```

## Reading the state
Partial scheduling has no explicit state. The model is marked `ModelAvailable` and is ready to serve. Inspect the Model CR (`kubectl get model`) and compare the columns `DESIRED REPLICAS` and `AVAILABLE REPLICAS`:

- Fully scheduled: READY is True and desired equals available (status `ModelAvailable`).
- Partially scheduled: READY is True and desired is greater than available (status `ModelAvailable`).
- Not scheduled: READY is False (status `ScheduleFailed`).

A model that cannot reach `minReplicas` remains `ScheduleFailed`.

## Checked

2026-11-04. Confirmed against models/scheduling.md (Seldon Core 2 docs, v2 branch): from 2.9, minReplicas, status logic table. Removed or corrected: nothing.

Method: documentation only; no commands were run.
