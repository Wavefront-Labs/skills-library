---
id: computing-software.ai-ml-engineering.kserve.kserve-llmisvc-router-scheduler
name: kserve-llmisvc-router-scheduler
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [router, httproute, inferencepool, endpointpickerconfig, epp, scheduler, prefix-cache-scorer, load-aware-scorer, gateway-refs, url-rewrite, timeouts]
level: advanced
status: docs-checked
description: "Configure LLMInferenceService router: managed or referenced Gateway and HTTPRoute, custom route rules, InferencePool ref/spec, EndpointPickerConfig inline or ref, and precedence."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/generative-inference/llmisvc/llmisvc-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LLMInferenceService router and scheduler

`spec.router` has `gateway`, `route`, `scheduler`; `{}` means managed by KServe.

- Gateway: `gateway: {refs: [{name: my-custom-gateway, namespace: istio-system}]}` uses an existing Gateway.
- HTTPRoute: `route.http.refs` brings your own route (controller only validates it exists); `route.http.spec` makes the controller create one with your rules. `spec` and `refs` are mutually exclusive. Uses: `timeouts: {request: "300s", backendRequest: "300s"}`, `URLRewrite` with `ReplacePrefixMatch`, or a `Service` backendRef to bypass the InferencePool.

## Scheduler
Managed scheduler creates an InferencePool, InferenceModel, scheduler Deployment (EPP) and Service. `scheduler.pool.ref.name` uses an existing pool (no EPP or pool created, only the InferenceModel); `scheduler.pool.spec` (selector, `targetPort`) customises one; `ref` and `spec` exclusive.

## EndpointPickerConfig
Default plugins are generated per topology. Override with exactly one of:
```yaml
scheduler:
  config:
    inline:
      apiVersion: llm-d.ai/v1alpha1
      kind: EndpointPickerConfig
      plugins: [{type: single-profile-handler}, {type: prefix-cache-scorer}, {type: max-score-picker}]
      schedulingProfiles: [{name: default, plugins: [{pluginRef: prefix-cache-scorer, weight: 2.0}, {pluginRef: max-score-picker}]}]
    # or: ref: {name: my-epp-config, key: epp}
```
`ref` names a ConfigMap in the service namespace (names prefixed `config-scheduler-` fall back to the KServe namespace); `key` is required; editing it rolls the EPP. Precedence: `scheduler.config`, then `--config-text`/`--config-file` on the `main` container in `scheduler.template`, then the running EPP flag, then the generated default. `predicted-latency-producer`, `token-producer` and `precise-prefix-cache-scorer` need `inline`; through `ref` the supporting preset is never merged in. `inline` and `ref` are mutually exclusive.

## Checked
Confirmed against the KServe LLMInferenceService configuration guide: router gateway, route and scheduler options, mutual exclusivity of spec and refs, pool ref and spec behaviour, EndpointPickerConfig inline and ref forms, ConfigMap lookup rules, precedence order and the inline-only plugin warning.

Method: docs-only read of cited pages, 2026-11-08
