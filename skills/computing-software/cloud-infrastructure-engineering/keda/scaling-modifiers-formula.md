---
id: computing-software.cloud-infrastructure-engineering.keda.scaling-modifiers-formula
name: scaling-modifiers-formula
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [scalingmodifiers, formula, composite-metric, expr-language, ternary, activationtarget]
level: advanced
status: docs-checked
description: "Combine several KEDA triggers into one scaling metric with advanced.scalingModifiers formulas, including averages, ternary conditions and count."
sources:
  - https://keda.sh/docs/2.17/concepts/scaling-deployments/
  - https://keda.sh/docs/2.17/reference/scaledobject-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`advanced.scalingModifiers` creates a composite metric for the HPA that replaces all external-metric requests and is computed inside KEDA. `target` and `formula` are mandatory; `activationTarget` (default 0) and `metricType` (`AverageValue` default, or `Value`) are optional. Every trigger used in the formula must have a `name`. Formulas use the `expr` language, must return a single non-boolean value and are internally cast to float. While the fallback feature is in effect the formula does not modify metrics, so it applies only when all triggers are healthy.

Examples from the page:

```yaml
advanced:
  scalingModifiers:
    formula: "(trig_one + trig_two)/2"
    target: "2"
    activationTarget: "2"
    metricType: "AverageValue"
```
averages a `kubernetes-workload` trigger named `trig_one` and a `metrics-api` trigger named `trig_two`.

- Ternary: `trig_one > 2 ? trig_one + trig_two : 1`
- Count: `count([trig_one,trig_two,trig_three],{#>1}) > 1 ? 5 : 0` returns 5 when at least two metrics exceed 1.
- Nested: `trig_one < 2 ? trig_one+trig_two >= 2 ? 5 : 10 : 0`

If the computed value is at or below `activationTarget`, the ScaledObject is not Active and may go to 0.

## Checked

2026-11-03. Confirmed on the 2.17 Scaling Deployments and ScaledObject specification pages: field requirements, defaults, the example formulas, fallback interaction.

Method: documentation only; no commands were run.
