---
id: computing-software.ai-ml-engineering.seldon-core-2.experiments-sticky-sessions
name: experiments-sticky-sessions
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, experiment, sticky-sessions, x-seldon-route, seldon-model-header, service-mesh-split]
level: advanced
status: docs-checked
description: "Keep a client on the same experiment branch in Seldon Core 2 by sending back the x-seldon-route response header with seldon-model, and know the replica-level caveat."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/kubernetes/resources/experiment.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Experiment sticky sessions

To give cohorts a consistent view during an experiment, every inference response carries the header `x-seldon-route`. Send that header on later requests to the experiment to bypass the random traffic split and get a prediction from the same sequence of models and pipelines used in the first request.

## Rules
- You must also send the normal `seldon-model` header together with `x-seldon-route`.
- Capture it from the first response and replay it unchanged.

```bash
curl http://${MESH_IP}/v2/models/experiment-iris/infer \
   -H "Content-Type: application/json" \
   -H "seldon-model: experiment-iris.experiment" \
   -H "x-seldon-route: <value from the first response>" \
   -d @request.json
```

## Caveat
The same models are used, but not necessarily the same replica instances. Sticky sessions therefore do not work for stateful models that need the same model replica.

## Alternative
If you use a service mesh that supports header-based routing in traffic splits, you can run experiments at mesh level instead.

## Checked

Confirmed against the Experiments page (Sticky Sessions section): the x-seldon-route response header, bypassing the random split, the requirement to also send seldon-model, the replica caveat for stateful models, and the service-mesh alternative. Removed the sample header value, which the page does not show.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb kubernetes/resources/experiment.md page (raw markdown).
