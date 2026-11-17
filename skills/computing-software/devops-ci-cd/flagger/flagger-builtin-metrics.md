---
id: computing-software.devops-ci-cd.flagger.flagger-builtin-metrics
name: flagger-builtin-metrics
category: computing-software
field: devops-ci-cd
product: flagger
tags: [metrics, builtin-metrics, thresholdrange, request-success-rate]
level: intro
status: docs-checked
description: "Use the two builtin Flagger metric checks, request-success-rate and request-duration, with thresholdRange and interval."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/metrics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flagger validates service level objectives during analysis and rolls back if performance drops. Two checks are built in, available for every mesh and ingress controller and implemented as Prometheus queries:

```yaml
analysis:
  metrics:
  - name: request-success-rate
    interval: 1m
    # minimum req success rate (non 5xx responses), percentage 0-100
    thresholdRange:
      min: 99
  - name: request-duration
    interval: 1m
    # maximum req duration P99, milliseconds
    thresholdRange:
      max: 500
```

`thresholdRange` is the accepted range (`min`, `max` or both) and `interval` is the time-series window. Success rate counts non-5xx responses; duration is P99 in milliseconds. A failing check halts advancement and increments the failed checks counter; reaching `threshold` rolls back. Because the builtin queries differ per provider, the FAQ documents the Prometheus expression used for each mesh.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/metrics.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
