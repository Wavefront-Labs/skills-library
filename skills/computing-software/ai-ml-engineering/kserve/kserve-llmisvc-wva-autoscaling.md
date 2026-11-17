---
id: computing-software.ai-ml-engineering.kserve.kserve-llmisvc-wva-autoscaling
name: kserve-llmisvc-wva-autoscaling
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [wva, specscaling, variantautoscaling, variantcost, wva-desired-replicas, idlereplicacount, initialcooldownperiod, autoscaling-wva-controller-config, prometheus-adapter]
level: advanced
status: docs-checked
description: "Autoscale LLMInferenceService with the Workload Variant Autoscaler: spec.scaling min/max/wva, HPA vs KEDA actuator, KEDA options, Prometheus config key, prefill scaling."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/generative-inference/llmisvc/autoscaling/llmisvc-autoscaling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LLMInferenceService autoscaling with WVA

`spec.scaling` makes KServe create a `VariantAutoscaling` CR (llm-d workload-variant-autoscaler) plus an actuator (HPA or KEDA ScaledObject). WVA computes replicas from inference metrics and publishes Prometheus metric `wva_desired_replicas`; the actuator (target=1) just applies it. `spec.scaling` and `spec.replicas` are mutually exclusive. Choose exactly one of `hpa` or `keda`.

The page's full examples use `apiVersion: serving.kserve.io/v1alpha2`.

```yaml
spec:
  scaling:
    minReplicas: 2
    maxReplicas: 8
    wva:
      variantCost: "10.0"
      keda:
        pollingInterval: 5
        cooldownPeriod: 120
        initialCooldownPeriod: 60   # covers model load time
        idleReplicaCount: 1         # must be less than minReplicas
        fallback: {failureThreshold: 3, replicas: 2}
```
HPA form: `wva: {hpa: {}}` or `hpa.behavior` (standard HorizontalPodAutoscalerBehavior with scaleUp/scaleDown).

| | HPA | KEDA |
|---|---|---|
| Needs | Prometheus Adapter with external metric rule for `wva_desired_replicas` | KEDA operator |
| Idle scale-down | no (min 1) | `idleReplicaCount` |
| Metric outage | HPA Unknown | `fallback` replicas |

## Prerequisites
WVA controller; Prometheus scraping inference pods and WVA. KEDA only: key `autoscaling-wva-controller-config` in ConfigMap `inferenceservice-config` (kserve namespace):
```json
{"prometheus": {"url": "https://prometheus-kube-prometheus-prometheus.monitoring:9090", "tlsInsecureSkipVerify": true, "authModes": "bearer", "triggerAuthName": "prometheus-auth", "triggerAuthKind": "ClusterTriggerAuthentication"}}
```
`url` required; `authModes` and `triggerAuthName` set together or both empty; `triggerAuthKind` defaults to `TriggerAuthentication`.

## Prefill
Scale a disaggregated prefill pool with `spec.prefill.scaling`; decode and prefill must use the same actuator backend. Conditions: `ScalingReady`, `PrefillScalingReady`. The controller creates separate VariantAutoscaling and actuator resources for each workload.

Setting the `serving.kserve.io/stop` annotation makes the controller delete the VariantAutoscaling, HPA and KEDA ScaledObject and clear the scaling conditions; they are recreated when it is removed. Validation errors seen when `scaling` is set without `wva`, together with `replicas`, or with mixed actuators between decode and prefill.

## Checked
Confirmed against the KServe Autoscaling LLMInferenceService with WVA page: spec.scaling behaviour and exclusivity with spec.replicas, the actuator comparison table, HPA and KEDA example fields, idleReplicaCount and initialCooldownPeriod notes, the autoscaling-wva-controller-config key and field table, prefill scaling and condition names, and the force-stop behaviour. The example Prometheus URL is the page's sample value, not a default.

Method: docs-only read of cited pages, 2026-11-08
