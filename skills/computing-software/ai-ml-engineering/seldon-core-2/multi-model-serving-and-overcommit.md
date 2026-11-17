---
id: computing-software.ai-ml-engineering.seldon-core-2.multi-model-serving-and-overcommit
name: multi-model-serving-and-overcommit
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, multi-model-serving, mms, overcommit, lru, seldon-overcommit-percentage, agent, memory]
level: practitioner
status: docs-checked
description: "Multi-model serving shares one MLServer or Triton among models; overcommit registers more models than fit in memory, evicting least recently used (SELDON_OVERCOMMIT_PERCENTAGE)."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/models/mms.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multi-model serving and overcommit

## Multi-model serving
One inference server hosts several models under different paths. MLServer and Triton both support this. Models share hardware such as a GPU, instead of one model per server. It is the default in Core 2: the Scheduler matches the Model `requirements` to Server capabilities and picks a replica with enough memory.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Model
metadata:
  name: tfsimple1
spec:
  storageUri: "gs://seldon-models/triton/simple"
  requirements:
  - tensorflow
  memory: 100Ki
```

## Overcommit
Overcommit lets a shared server register more models than fit in memory, keeping busy models loaded and evicting others to disk with a least-recently-used (LRU) policy. All models still show as ready.

- Controlled by `SELDON_OVERCOMMIT_PERCENTAGE` on the shared server, default 10.
- Registered memory limit: MEMORY_REQUEST times (1 + SELDON_OVERCOMMIT_PERCENTAGE / 100).
- Set it to 0 to disable overcommit on that server.
- The Agent sidecar tracks inference times per model and evicts the least recently used one on a new load beyond capacity, or when a request arrives for an evicted model.
- A reload uses the artifact cached on disk (no remote fetch); expect extra latency with a lower bound of about 100ms.

Memory values come from what you set on the Server and the Model; Core 2 does not yet manage memory automatically.

## Checked

2026-11-04. Confirmed against models/mms.md (Seldon Core 2 docs, v2 branch): MMS behaviour, overcommit default 10, formula, LRU by Agent, ~100ms lower bound, disable with 0. Removed or corrected: nothing.

Method: documentation only; no commands were run.
