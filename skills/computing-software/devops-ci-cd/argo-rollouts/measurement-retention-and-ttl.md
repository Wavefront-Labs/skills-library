---
id: computing-software.devops-ci-cd.argo-rollouts.measurement-retention-and-ttl
name: measurement-retention-and-ttl
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [measurementretention, ttlstrategy, analysisrun, history, cleanup, analysis, argo-rollouts]
level: practitioner
status: docs-checked
description: "Keep more than ten measurements per metric and expire finished AnalysisRuns with measurementRetention and ttlStrategy."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
  - https://argo-rollouts.readthedocs.io/en/stable/features/specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Measurement retention.** By default the controller keeps the latest ten measurements per metric. Since v1.2, `measurementRetention` overrides that per metric (dry-run or not). Setting the option to 0 disables it and reverts to the default ten. Regex names work, so `.*` applies to all metrics.

```yaml
spec:
  measurementRetention:
    - metricName: total-5xx-errors
      limit: 20
```

A Rollout specifies `measurementRetention` on its analysis stanza (the docs example is an `analysis` step with `metricName: .*` and `limit: 20`); an Experiment specifies it under its spec, for example `metricName: test.*`.

**Custom metadata.** `analysisRunMetadata` on the analysis stanza (or an experiment step) attaches labels and annotations to the generated AnalysisRun, for example an external link annotation.

**TTL.** Since v1.7, `ttlStrategy` on an AnalysisRun deletes it after a time to live once it has finished, depending on whether it succeeded or failed:

```yaml
spec:
  ttlStrategy:
    secondsAfterCompletion: 3600
    secondsAfterSuccess: 1800
    secondsAfterFailure: 1800
```

If unset, completed runs are kept unless the owning Rollout applies its own garbage collection through `analysis.successfulRunHistoryLimit` and `unsuccessfulRunHistoryLimit` (both default 5).

Verify with `kubectl get analysisrun` after the TTL passes.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/analysis/, https://argo-rollouts.readthedocs.io/en/stable/features/specification/.

Removed or corrected: the claim of a strategy.canary.analysis.measurementRetention path and blueGreen equivalents; the page example is an analysis step.

Method: documentation only; no commands were run.
