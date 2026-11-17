---
id: computing-software.devops-ci-cd.flux.helmchart-version-and-reconcile-strategy
name: helmchart-version-and-reconcile-strategy
category: computing-software
field: devops-ci-cd
product: flux
tags: [helmchart, reconcilestrategy, valuesfiles, version, semver]
level: advanced
status: docs-checked
description: "Control HelmChart version ranges, valuesFiles and reconcileStrategy ChartVersion versus Revision for Git and Bucket charts."
sources:
  - https://fluxcd.io/flux/components/source/helmcharts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A HelmChart builds a chart artifact from a source. HelmReleases normally create it for you via `.spec.chart.spec`, which accepts the same fields.

`.spec.chart` is the chart name for a HelmRepository source, or the chart directory path for GitRepository and Bucket sources:

```yaml
spec:
  chart: ./charts/podinfo
  sourceRef:
    name: podinfo
    kind: GitRepository
```

`.spec.version` only applies to a HelmRepository source and defaults to `*`, the latest. It can be fixed, a patch range such as `4.0.x`, or a range like `>=4.0.0 <5.0.0`. Git and Bucket sources ignore it.

`.spec.reconcileStrategy`:
- `ChartVersion` (default): a new artifact appears when the chart version changes.
- `Revision`: a new artifact appears when the source revision changes (Git or Bucket).

Gotcha: with `ChartVersion` and a Git or Bucket source, changes to templates do not produce a new chart artifact unless `version` in `Chart.yaml` is bumped. Use `Revision` for charts that live in Git next to the app and are not versioned per commit.

`.spec.valuesFiles` lists alternative values files, relative to the source, merged in order with the last winning. The chart is then packaged with those values. Both strategy and values files affect the artifact revision.

`.spec.ignoreMissingValuesFiles` tolerates absent files. Signature verification (`.spec.verify` with cosign or notation) works only for charts fetched from an OCI registry.

## Checked

2026-11-03. Read the HelmChart reference (fluxcd.io/flux/components/source/helmcharts/): `.spec.version` default `*` and range forms, `reconcileStrategy` ChartVersion/Revision and the Git/Bucket note, `valuesFiles`, `ignoreMissingValuesFiles`, and `.spec.verify` available only for OCI-fetched charts. Nothing removed.

Method: documentation only; no commands were run.
