---
id: computing-software.cloud-infrastructure-engineering.knative.kpa-panic-mode
name: kpa-panic-mode
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [panic-mode, stable-window, panic-window-percentage, panic-threshold-percentage, max-scale-up-rate]
level: advanced
status: docs-checked
description: "Tune the KPA stable window, panic window, panic threshold and scale rates."
sources:
  - https://knative.dev/docs/serving/autoscaling/kpa-specific/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune how the KPA reacts to steady load versus bursts.

The KPA runs in two modes with separate aggregation windows. Stable mode is used in general operation. Panic mode has a much shorter window and scales a Revision up quickly when a burst arrives. In panic mode the Revision does not scale down, avoiding churn; the autoscaler leaves panic mode after no reason to react quickly for a stable window.

Settings (global key / annotation under `autoscaling.knative.dev/`):
- Stable window: `stable-window` / `window`, `6s` to `1h`, default `60s`. When scaling to zero, the last replica goes only after no traffic for the full window.
- Panic window: `panic-window-percentage` / `panic-window-percentage`, float `1.0` to `100.0`, default `10.0`. It is a percentage of the stable window, so `10.0` means the panic window is 10 percent of it.
- Panic threshold: `panic-threshold-percentage` / same name, float `110.0` to `1000.0`, default `200.0`.
- Max scale up rate: `max-scale-up-rate`, float, default `1000.0`, global only.
- Max scale down rate: `max-scale-down-rate`, float, default `2.0`, global only.

```yaml
data:
  stable-window: "40s"
```

The same keys can be set through the Operator under `spec.config.autoscaler`.

## Checked

2026-11-03. Confirmed on the Knative Serving autoscaling/kpa-specific page: stable and panic modes, windows, thresholds, scale rates and defaults. Removed: nothing.
Method: documentation only; no commands were run.
