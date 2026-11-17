---
id: computing-software.ai-ml-engineering.kserve.kserve-llmisvc-status
name: kserve-llmisvc-status
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [status, conditions, workloadsready, routerready, presetscombined, mainworkloadready, inferencepoolready, groupready, reason-codes]
level: advanced
status: docs-checked
description: "LLMInferenceService status contract: Ready rollup of WorkloadsReady and RouterReady, sub-conditions per topology, PresetsCombined gate, group conditions and status.router.group."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/generative-inference/llmisvc/llmisvc-status.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LLMInferenceService status reference

`Ready` = `WorkloadsReady` AND `RouterReady` (Knative LivingConditionSet). All conditions use positive polarity. `PresetsCombined` is a separate gate, not in the rollup: if baseRef resolution fails the reconciler stops before workloads and router.

## Workload sub-conditions
- `MainWorkloadReady`: single-node Deployment (cleared in multi-node).
- `WorkerWorkloadReady`: LeaderWorkerSet available (multi-node).
- `PrefillWorkloadReady`, `PrefillWorkerWorkloadReady`: prefill-decode and multi-node prefill-decode.
- `ScalingReady`, `PrefillScalingReady`: HPA, KEDA ScaledObject or VariantAutoscaling operational.

## Router sub-conditions
`GatewaysReady` (gateway refs), `HTTPRoutesReady` (route accepted by parents), `InferencePoolReady` and `SchedulerWorkloadReady` (managed scheduler). Absent features clear the condition rather than setting True.

## Identify topology from status
`status.workloads.primary.kind` is `Deployment` or `LeaderWorkerSet`; `status.workloads.prefill` populated means disaggregated; `status.router.scheduler` and `status.workloads.scheduler` mean a managed scheduler.

## Config reasons (PresetsCombined)
`ConfigNotFound`: referenced `LLMInferenceServiceConfig` not in any searched namespace (controller recovers when created). `CombineBaseError`: merge conflict, read the message and review `baseRefs`.

## Group conditions
`GroupReady` and `GroupDegraded` are independent of `Ready`; present only with `spec.router.route.group`. `GroupDegraded` (`MemberDivergence`) means members have different model names or LoRA sets. `status.router.group` lists `name` and `members[]` with `name`, `weight`, `stopped` (force-stop annotation) and `backendRef` (an InferencePool).

## Checked

Checked 2026-11-08 against the KServe website page llmisvc-status.md, read through the status fields and sample status (the condition hierarchy, topology signals, condition tables, config reasons, group conditions and status.router.group, status.workloads and appliedConfigs). Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
