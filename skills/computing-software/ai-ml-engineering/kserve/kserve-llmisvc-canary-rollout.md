---
id: computing-software.ai-ml-engineering.kserve.kserve-llmisvc-canary-rollout
name: kserve-llmisvc-canary-rollout
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [canary, routing-group, group, weight, servingkserveiostop, groupdegraded, memberdivergence, weighted-backendref, v1alpha2]
level: advanced
status: docs-checked
description: "Canary rollout across LLMInferenceServices with spec.router.route group and weight: ramp by patching weight, promote by stop annotation, rollback, dark-deploy warning."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/generative-inference/llmisvc/canary-rollout.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LLMInferenceService canary rollout

Each version is its own LLMInferenceService. Members share `spec.router.route.group` and declare a proportional `weight` (9 and 1 gives 90/10; 9 and 9 gives 50/50). No primary/canary distinction; all members are symmetric. A webhook sets label `serving.kserve.io/routing-group`; every member's HTTPRoute carries the weighted backendRefs of all non-stopped members.

```yaml
spec:
  model: {name: my-model, uri: hf://meta-llama/Llama-3.1-70B}
  router:
    route: {group: my-model, weight: 1}
    scheduler: {}
```

Members must have the same `model.name` and LoRA adapter set, otherwise `GroupDegraded=True` reason `MemberDivergence`.

## Lifecycle
1. Deploy v1 (weight 9), then v2 with the same group and weight 1.
2. Compare e.g. P95 `vllm:time_to_first_token_seconds_bucket` per `llm_isvc_name`.
3. Ramp: `kubectl patch llmisvc my-model-v2 --type merge -p '{"spec":{"router":{"route":{"weight":9}}}}'` (only patch the changed version; no pod restart).
4. Promote: `kubectl annotate llmisvc my-model-v1 serving.kserve.io/stop=true` scales it to zero, status shows `stopped: true`, weight kept.
5. Rollback: lower v2 weight, or `kubectl annotate llmisvc my-model-v1 serving.kserve.io/stop-` and wait for Ready.
6. Decommission with `kubectl delete llmisvc my-model-v1`.

Warning: avoid `weight: 0` dark deploys; the gateway may not warm the backend and raise transient connection failures later. Start at 1. Reach a version directly at `/<namespace>/<name>/v1/completions` regardless of weights.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited canary rollout page in full; group/weight semantics, lifecycle commands, dark-deploy warning and direct access path all match. No content removed.
