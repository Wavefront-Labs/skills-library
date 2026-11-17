---
id: computing-software.ai-ml-engineering.kserve.kserve-llmisvc-config-composition
name: kserve-llmisvc-config-composition
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [baserefs, llminferenceserviceconfig, config-composition, strategic-merge-patch, kserve-config-llm-template, kserve-config-llm-scheduler, kserve-config-llm-router-route, well-known-configs]
level: advanced
status: docs-checked
description: "How the LLMInferenceService controller merges well-known configs, baseRefs LLMInferenceServiceConfig and the spec by strategic merge patch, and which config applies per topology."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/generative-inference/llmisvc/llmisvc-config-composition.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LLMInferenceService config composition

The controller builds an effective config by strategic merge patch in a fixed order, later wins: well-known configs (platform, lowest) then each `spec.baseRefs` entry in order (`LLMInferenceServiceConfig` resources, middle) then the `LLMInferenceService` spec (highest).

```yaml
spec:
  baseRefs:
    - name: my-gpu-profile   # looked up in the service namespace, then the kserve namespace
  model: {uri: hf://meta-llama/Llama-3.1-8B-Instruct, name: meta-llama/Llama-3.1-8B-Instruct}
  replicas: 3              # overrides baseRef replicas: 2
  router: {route: {}, scheduler: {}}
```

## Injected well-known configs
| Spec shape | Config |
|---|---|
| no prefill, no worker | `kserve-config-llm-template` |
| worker + data parallel | `kserve-config-llm-worker-data-parallel` |
| prefill, no worker | `kserve-config-llm-prefill-template` + `kserve-config-llm-decode-template` |
| prefill + worker | `kserve-config-llm-prefill-worker-data-parallel` + `kserve-config-llm-decode-worker-data-parallel` |
| `router.scheduler` without external pool ref | `kserve-config-llm-scheduler` |
| `router.route` without external route refs | `kserve-config-llm-router-route` |

Workload paths are mutually exclusive; router configs combine with any.

## Merge rules
- Non-zero override fields apply; zero values (`""`, 0, nil, false) never overwrite base values.
- Containers merge by name, so `main` from each source becomes one `main`; each of `template`, `worker`, `prefill` has its own `main`.
- In a baseRef set only the fields you change (for example just `resources.limits` with `nvidia.com/gpu`); image and ports are preserved.

## Namespace resolution
Each config reference (well-known or baseRef) is looked up in the service namespace first, then the KServe system namespace (typically `kserve`). If neither has it, `PresetsCombined` is set False with reason `ConfigNotFound`, which blocks reconciliation. `status.appliedConfigs` records each config used, tagged `Preset` (well-known) or `UserRef` (baseRef). A same-name config in a team namespace overrides the shared one.

## Checked

Checked 2026-11-08 against the KServe website page llmisvc-config-composition.md, read in full: merge order, the injection tables, strategic merge rules, namespace resolution, PresetsCombined/ConfigNotFound and appliedConfigs. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
