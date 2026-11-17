---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.canary-metrics-selection-and-evaluation
name: canary-metrics-selection-and-evaluation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [canary-metrics-selection, canary-evaluation, canary-analysis, kayenta, argo-rollouts, analysis-template]
level: advanced
status: docs-checked
description: "Pick canary metrics that indicate user harm and separate canary from control, then evaluate automatically with Argo Rollouts analysis, drawing on the SRE Workbook."
sources: ["https://sre.google/workbook/canarying-releases/", "https://argo-rollouts.readthedocs.io/en/stable/features/analysis/", "https://github.com/spinnaker/kayenta"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selecting and evaluating canary metrics

The Workbook says the canary process demonstrates value when it detects bad release candidates with high
confidence and identifies good releases without false positives. Too many or noisy metrics produce false
positives that train people to ignore the canary.

## Choosing metrics
- The representativeness of a canary is tightly connected to the metrics you evaluate. Trivial metrics such as
  query success can be evaluated quickly; others, such as queue depth, may need more time or a larger canary
  population to give a clear signal.
- Compare canary signals with control signals, and structure monitoring so that comparison is straightforward.
  The Workbook's example: a 5% canary running a 20% error rate looks like only a 1% error rate to whole-system
  monitoring, which may be indistinguishable from other errors. So label metrics by version so canary and control separate.
- Time-limited canaries interact badly with metrics aggregated over a period (the Workbook's errors-per-hour example).
- Also check absolute measures such as SLOs, because the canary can affect the control through imperfect isolation.
- Avoid metrics from shared downstreams: they are not attributable to the canary.

## Argo Rollouts analysis
Per the Argo Rollouts analysis page:
- An `AnalysisTemplate` defines how to perform a canary analysis: the metrics, their frequency and the values
  considered successful or failed; it can be parameterised with arguments.
- An `AnalysisRun` is an instantiation of a template. Completed runs are Successful, Failed or Inconclusive, which
  make the rollout continue, abort or pause respectively.
- A rollout's canary analysis can use `startingStep` to delay starting the run until a given step; a metric can set
  `failureLimit`; with no interval, an analysis takes a single measurement and completes.
- An `Experiment` can run a baseline and a canary in parallel and compare their metrics for an equal comparison.
- Treat missing data (no traffic yet) as inconclusive rather than a pass; read the page for how your version
  expresses that.
- Kayenta (the Spinnaker project) is an automated canary analysis service; read its repository for judges and scoring.

## Verify
- [ ] An injected fault in the canary build fails the analysis.
- [ ] A no-op release passes repeatedly (false-positive rate measured).

## Checked

2026-11-01. Confirmed against the SRE Workbook chapter Canarying Releases (detection with high confidence and no
false positives, metric choice tied to representativeness, trivial versus slow metrics, canary-versus-control
comparison, the 5% and 20% example, errors-per-hour pitfall, imperfect isolation) and the Argo Rollouts analysis
page (AnalysisTemplate, AnalysisRun outcomes, startingStep, failureLimit, Experiment). The Kayenta repository page
confirms only that it exists. Removed: the Mann-Whitney and score 75 claims, the full YAML with its Prometheus
query, the 1.2x threshold, the label names and inconclusiveLimit.
Method: documentation only; no commands were run.
