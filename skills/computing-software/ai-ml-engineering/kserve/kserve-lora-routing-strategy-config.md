---
id: computing-software.ai-ml-engineering.kserve.kserve-lora-routing-strategy-config
name: kserve-lora-routing-strategy-config
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [loramodelroutingstrategy, servingkserveiolora-model-routing-strategy, modelbasedroutingmode, servingkserveiomodel-based-routing-enabled, modelbasedroutingheadername, x-gateway-model-name, re2max-program-size, routingpreconditionnotmet, regex-routing]
level: advanced
status: docs-checked
description: "Route many LoRA adapters through gateway HTTPRoutes: exact vs regex strategy, model-based routing prerequisites, Gateway API 64-match limit, and Envoy RE2 program-size limits."
sources: ["https://github.com/kserve/website/blob/main/docs/admin-guide/configurations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LoRA model routing strategy

Setting `loraModelRoutingStrategy` in the `ingress` JSON of `inferenceservice-config` (Helm: `kserve.controller.gateway.loraModelRoutingStrategy` in `kserve-resources` and `kserve-llmisvc-resources`) is `exact` (default, one match per adapter) or `regex` (base model and adapters grouped into shared regex matches). Per-LLMInferenceService override: `spec.annotations["serving.kserve.io/lora-model-routing-strategy"]`, also usable via an LLMInferenceServiceConfig preset; empty inherits the cluster value. The controller watches the ConfigMap, no restart needed; an unsupported value stops ingress config loading.

## Prerequisites (model-based routing)
- `modelBasedRoutingMode` in `ingress`: `enabled` (default), `disabled` (removes model-header matches) or `forced` (ignores a Gateway opt-out; a Gateway opts out with annotation `serving.kserve.io/model-based-routing-enabled: "false"`).
- The service needs `serving.kserve.io/model-based-routing-enabled: "true"` in its effective `spec.annotations`, even when forced.
- Clients send the header named by `modelBasedRoutingHeaderName` (default `X-Gateway-Model-Name`) or the gateway derives it from the body.
- Custom routes: the header match must be `Exact` on `publishers/<namespace>/models/<base-model-name>`, else status `RoutingPreconditionNotMet`.

## Capacity
The shipped template uses 8 header matches per model; Gateway API allows 64 per rule, so `exact` fits the base plus 7 adapters while `regex` stays at 8. Each header pattern is capped at 4096 characters.

## Envoy RE2 limit
Envoy rejects regexes above `re2.max_program_size.error_level` (Envoy's own default 100; Envoy Gateway 1.8.1 default bootstrap 4294967295, effectively disabling the check; Istio 1.30.3 default bootstrap 32768). `warn_level` only produces warnings. A rejection shows as an xDS NACK while the HTTPRoute still says `Accepted=True`, so check proxy logs for `RE2 program size`. Inspect via admin `GET /runtime` on port 19000 for Envoy Gateway (Istio 15000). In Envoy Gateway raise it with an `EnvoyProxy` bootstrap JSONPatch (`op: add`) on `/layered_runtime/layers/0/static_layer/re2.max_program_size.error_level`; the page's example value 32768 is only an example, and the path is for Envoy Gateway 1.8.1's default bootstrap, so verify it for your version.

## Checked
Confirmed against the KServe admin guide configurations page (LoRA Model Routing Strategy section): config keys, Helm values, annotation override and inheritance, model-based routing prerequisites, route capacity numbers, Envoy limits table and inspection and patch steps.

Method: docs-only read of cited pages, 2026-11-08
