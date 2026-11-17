---
id: computing-software.devops-ci-cd.argo-events.argo-events-sensor-trigger-conditions-expressions
name: argo-events-sensor-trigger-conditions-expressions
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, trigger-conditions, conditions, dependencies, boolean-expression, sensor]
level: practitioner
status: docs-checked
description: "Gate each Sensor trigger on a boolean expression of dependency names using AND and OR operators, with the all-dependencies default."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/trigger-conditions.md", "https://github.com/argoproj/argo-events/blob/master/docs/sensors/more-about-sensors-and-triggers.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events sensor trigger conditions expressions

From v1.0, a trigger template can carry `conditions`, a boolean expression over dependency names. The trigger does not run until it resolves to true. Supported operators are `&&` and `||`, with parentheses.

```yaml
spec:
  dependencies:
    - name: dep01
      eventSourceName: webhook-a
      eventName: example01
    - name: dep02
      eventSourceName: webhook-a
      eventName: example02
    - name: dep03
      eventSourceName: webhook-b
      eventName: example03
  triggers:
    - template:
        conditions: "(dep01 || dep02) && dep03"
        name: trigger03
        http:
          url: http://abc.com/hello3
          method: GET
```

Other triggers in the same Sensor can use different conditions, such as `"dep02"` or `"dep02 && dep03"`.

If `conditions` is omitted, the default is `&&` of every dependency defined in the Sensor: the trigger waits for all of them.

When the conditions resolve to true, the latest event from each dependency is used. With `A && B`, if A received a1 to a10 before B's b1 arrived, a10 and b1 fire the trigger and a1 to a9 are dropped (More About Sensors And Triggers page).

## Checked

2026-11-04. Confirmed against the Trigger Conditions page (v1.0 and after, a boolean expression of dependency names, operators `&&` and `||`, the three-dependency example including `(dep01 || dep02) && dep03`, and the default of `&&` over all dependencies) and the More About Sensors And Triggers page (latest event per dependency, the a1-a10 example). Removed a remark about fan-out that the pages do not state.
Method: documentation only; no commands were run.
