---
id: computing-software.ai-ml-engineering.seldon-core-2.experiments-ab-and-mirror
name: experiments-ab-and-mirror
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, experiment, ab-testing, canary, mirror, traffic-split, candidates, default-model, pipeline-experiment]
level: practitioner
status: docs-checked
description: "Split traffic between Seldon Core 2 Models or Pipelines with an Experiment: weighted candidates, a default model, a mirror, pipeline experiments and header calls."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/kubernetes/resources/experiment.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Experiments: A/B, canary and mirror

An Experiment defines a traffic split between Models or Pipelines, so new versions can be tested. The spec has three sections.

- `candidates` (required): models to split traffic across. Each has a weight; its share is that weight divided by the sum of weights.
- `default` (optional): an existing candidate whose endpoint is modified to carry the split.
- `mirror` (optional): one model that receives mirrored traffic; its responses are not returned to the caller.

## Default model
Splitting 50/50 between `iris` and `iris2` with `default` set to `iris` exposes the split on the existing `iris` endpoint. The experiment becomes active when both underlying models are Ready.

## New endpoint
Without `default`, the experiment gets its own endpoint. Call it with the header `seldon-model: <experiment-name>.experiment`:

```bash
curl http://${MESH_IP}/v2/models/experiment-iris/infer \
   -H "Content-Type: application/json" \
   -H "seldon-model: experiment-iris.experiment" \
   -d @request.json
```

where `request.json` holds a V2 payload such as `{"inputs": [{"name": "predict", "shape": [1, 4], "datatype": "FP32", "data": [[1, 2, 3, 4]]}]}`.

## Pipelines and mirrors
For pipelines set `resourceType: pipeline` so candidates or mirrors refer to pipelines. A mirror works for both models and pipelines, which suits shadow deployment: mirrored predictions are produced but never returned.

Experiments can also be run at the service mesh level if it supports header-based traffic splits.

## Checked

Confirmed against the Experiments page: the three spec sections, weight-share rule, default model behaviour and Ready condition, the .experiment header call, resourceType pipeline, mirror behaviour, and service-mesh alternative.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb kubernetes/resources/experiment.md page (raw markdown).
