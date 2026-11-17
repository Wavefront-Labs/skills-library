---
id: computing-software.ai-ml-engineering.kserve.kserve-v1-inference-protocol
name: kserve-v1-inference-protocol
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [v1-protocol, instances, inputs, predictions, v1models, model-ready, tensorflow-serving-api, list-models]
level: practitioner
status: docs-checked
description: "KServe V1 inference protocol: endpoints, instances/inputs request payloads, predictions/explanations responses, curl examples, benefits and limits versus V2."
sources: ["https://github.com/kserve/website/blob/main/docs/concepts/architecture/data-plane/v1-protocol.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# KServe V1 inference protocol

Based on the TensorFlow Serving REST API. Still supported, but V2 is recommended; keep V1 when you need `:explain` or a looser schema.

| API | Verb and path | Response |
|---|---|---|
| List models | GET /v1/models | `{"models": [name]}` |
| Model ready | GET /v1/models/NAME | `{"name": name, "ready": bool}` |
| Predict | POST /v1/models/NAME:predict | `{"predictions": []}` |
| Explain | POST /v1/models/NAME:explain | `{"predictions": [], "explanations": []}` |

Request root key is `instances` or `inputs` (equivalent). Rows can be objects of named feature arrays or plain nested lists:

```bash
curl -X POST http://localhost:8000/v1/models/mymodel:predict \
  -d '{"instances": [[1.0, 2.0, 5.0], [5.0, 6.0, 5.0]]}'
```

The response payload is not strictly enforced; custom servers may return their own, though the KServe shape is encouraged. Payload on list/ready calls is optional.

## Limits
Weakly standardised responses, inefficient for large payloads, no built-in health checking or readiness probes (as the page lists them), no binary data, little metadata. Explain is the functionality the page says is not available in V2.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited V1 protocol page in full. Removed the unsupported claim about plain Ingress in Standard mode and reworded the explain and health limitations to the page's wording.
