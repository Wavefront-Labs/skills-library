---
id: computing-software.cloud-infrastructure-engineering.knative.scale-bounds
name: scale-bounds
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [scale-bounds, min-scale, max-scale, initial-scale, scale-down-delay, activation-scale]
level: practitioner
status: docs-checked
description: "Configure min-scale, max-scale, initial-scale, activation-scale and scale-down-delay."
sources:
  - https://knative.dev/docs/serving/autoscaling/scale-bounds/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bound how far a Revision scales and how it starts.

Settings (global key / per-revision annotation under `autoscaling.knative.dev/`):
- Lower bound: `min-scale` / `min-scale`. Default `0` if scale to zero is enabled with the KPA class, else `1`.
- Upper bound: `max-scale` / `max-scale`. Default `0`, meaning unlimited.
- Initial scale: `initial-scale` (with `allow-zero-initial-scale`) / `initial-scale`. Default `1`.
- Scale up minimum: no global key / `activation-scale`. Default `1`.
- Scale down delay: `scale-down-delay` / `scale-down-delay`. Duration from `0s` to `1h`; default `0s`, no delay.
- Stable window: `stable-window` / `window`. Duration from `6s` to `1h`; default `60s`.

```yaml
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/min-scale: "3"
        autoscaling.knative.dev/max-scale: "10"
```

Knative tries never to run fewer than `min-scale` replicas, nor more than `max-scale` running or being created. Global values go in the `config-autoscaler` ConfigMap, for example `min-scale: "3"`. Initial scale is ignored once reached; the larger of initial scale (or activation scale) and the lower bound is the initial target. Scale down delay is supported only for the default KPA class.

## Checked

2026-11-03. Confirmed on the Knative Serving autoscaling/scale-bounds page: every key, annotation, range and default of the six settings. Removed: the per-revision-overrides sentence.
Method: documentation only; no commands were run.
