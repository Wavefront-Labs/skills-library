---
id: computing-software.devops-ci-cd.argo-rollouts.analysis-dry-run-mode
name: analysis-dry-run-mode
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [dryrun, analysis, metrics, regex, experiment, rollout, argo-rollouts]
level: advanced
status: docs-checked
description: "Evaluate new metrics without letting them affect rollout outcomes using dryRun on metrics, rollouts and experiments."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`dryRun` (since v1.2) evaluates a metric in dry-run mode: even if it fails or is inconclusive, it does not change the final state of the rollout or experiment. Use it to trial a new query in production before trusting it.

On an AnalysisTemplate, list metric names; regular expressions are supported, so `.*` puts every metric in dry-run:

```yaml
spec:
  dryRun:
    - metricName: total-5xx-errors
  metrics:
    - name: total-5xx-errors
      ...
```

If any metric runs in dry-run, a summary of dry-run results is appended to the AnalysisRun message, so you can see that, for example, `total-4xx-errors` would have failed while the run still passed.

For a Rollout, put `dryRun` under the strategy's `analysis` stanza; all metrics from the merged templates matching the names run in dry-run:

```yaml
strategy:
  canary:
    analysis:
      templates:
        - templateName: random-fail
        - templateName: always-pass
      dryRun:
        - metricName: .*
```

For an Experiment, put `dryRun` under its spec, for example `metricName: test.*` to cover matching metrics from the referenced template.

Verify: the AnalysisRun finishes Successful despite a failing dry-run metric, and its message contains the dry-run summary.

## Checked

2026-11-08. Confirmed against the Argo Rollouts analysis page (read in full from the docs source): dryRun since v1.2, regex metricName, dry-run summary appended to the AnalysisRun message, and the Rollout and Experiment forms.

Removed or corrected: nothing; claims matched.

Method: documentation only; no commands were run.
