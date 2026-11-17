---
id: computing-software.devops-ci-cd.argo-rollouts.analysis-nan-infinity-and-empty-results
name: analysis-nan-infinity-and-empty-results
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [nan, infinity, empty-result, isnan, isinf, default-function, successcondition, analysis, argo-rollouts]
level: advanced
status: docs-checked
description: "Write success and failure conditions that handle NaN, Infinity and empty query results deliberately."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Metric providers can return NaN, infinity or empty results. Decide explicitly how each should be judged, because the conditions are expr expressions evaluated against `result`.

NaN: the docs show three outcomes. Treat NaN as success:

```yaml
successCondition: isNaN(result) || result >= 0.95
```

Treat it as inconclusive or failed by writing the matching `failureCondition` or leaving success unmatched (no match means Inconclusive when conditions exist). Infinity can be failed with:

```yaml
failureCondition: isInf(result)
```

or accepted with a success expression using `isInf(result)`.

Empty arrays: a Prometheus query with no data returns an empty array, so `result[0]` would error. The docs show examples treating an empty array as success or as failure by testing the length of `result` in the condition.

Datadog: a query over an interval with no metrics yields a `nil` value, which produces an evaluation error. Handle it with the `default()` function:

```yaml
successCondition: default(result, 0) < 0.05
```

Pick the safe direction for your risk: for error-rate metrics, "no data" treated as success can hide an outage in the canary. Prefer making "no data" Inconclusive so a human checks.

Verify by running the template against a service with no traffic and confirming the AnalysisRun phase matches your intent.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/analysis/.

Removed or corrected: nothing; claims matched.

Method: documentation only; no commands were run.
