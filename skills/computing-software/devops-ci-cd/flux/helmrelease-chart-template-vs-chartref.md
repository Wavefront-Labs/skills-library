---
id: computing-software.devops-ci-cd.flux.helmrelease-chart-template-vs-chartref
name: helmrelease-chart-template-vs-chartref
category: computing-software
field: devops-ci-cd
product: flux
tags: [helmrelease, chart, chartref, ocirepository, helmchart]
level: sme
status: docs-checked
description: "Choose between spec.chart (template that creates a HelmChart or OCIRepository) and spec.chartRef (reference to an existing source)."
sources:
  - https://fluxcd.io/flux/components/helm/helmreleases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A HelmRelease gets its chart one of two ways.

`.spec.chart` is a template. helm-controller creates a source from `.spec.chart.spec`, named `<namespace>-<name>` of the HelmRelease. `.spec.chart.kind` is `HelmChart` (default, needs `chart` and `sourceRef`) or `OCIRepository` (needs `url`; HelmChart-only fields are rejected). A HelmChart is created in the sourceRef namespace, an OCIRepository in the HelmRelease namespace. With an OCIRepository and no `layerSelector`, the Helm chart layer is selected with the `copy` operation. The created resource is shown in `.status.helmChart`.

```yaml
spec:
  chart:
    spec:
      chart: podinfo
      version: "6.x"
      sourceRef:
        kind: HelmRepository
        name: podinfo
```

`.spec.chartRef` refers to an existing OCIRepository, HelmChart or (behind `--feature-gates=ExternalArtifact=true`) ExternalArtifact:

```yaml
spec:
  chartRef:
    kind: OCIRepository
    name: podinfo
```

With an OCIRepository the revision is reported as `<version>+<digest[0:12]>`, so a new digest triggers an upgrade even when `Chart.yaml` version is unchanged.

Trade-off: chartRef lets many HelmReleases share one source, but changing `.spec.values` and the chart version in one commit can cause a transient upgrade failure because the two sources update separately. The template avoids that. Do not set both fields.

Chart version of the last attempt is in `.status.lastAttemptedRevision`.

## Checked

2026-11-03. Read the HelmRelease reference (fluxcd.io/flux/components/helm/helmreleases/): chart template source naming and namespaces, `.status.helmChart`, default `copy` layer selection for OCIRepository, `.spec.chartRef` kinds incl. ExternalArtifact gate, `<version>+<digest[0:12]>`, the transient-failure trade-off and the one-of-both warning. Nothing removed.

Method: documentation only; no commands were run.
