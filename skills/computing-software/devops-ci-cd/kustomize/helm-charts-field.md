---
id: computing-software.devops-ci-cd.kustomize.helm-charts-field
name: helm-charts-field
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [helmcharts, helm, enable-helm, inflation]
level: advanced
status: docs-checked
description: "Inflate Helm charts inside a kustomization with helmCharts, which requires kustomize build --enable-helm and the helm binary."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/builtins/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`helmCharts` pulls and renders charts as part of a build. Enable it with a flag:

```bash
kustomize build --enable-helm
```

Entry fields documented on the built-ins page:

- `name`: the chart name.
- `repo` (optional): chart repository URL; if provided, remote charts are fetched, otherwise a local chart in `chartHome` is used.
- `version` (optional): chart version; latest if omitted.
- `releaseName`, `namespace` (passed as `--namespace` to `helm template`), `valuesFile`.
- `valuesInline`: values written in the kustomization; `valuesMerge` takes `merge`, `override` or `replace` (default `override`).
- `includeCRDs`: default `false`.
- `skipHooks`: skip running hooks; by default all templates are rendered, which can differ from `helm install`.
- `additionalValuesFiles`, `skipTests`, `apiVersions`, `nameTemplate`, `kubeVersion`.

```yaml
helmCharts:
- name: minecraft
  repo: https://kubernetes-charts.storage.googleapis.com
  version: v1.2.0
  releaseName: test
  namespace: testNamespace
  valuesFile: values.yaml
  additionalValuesFiles:
  - values-file-1.yml
  - values-file-2.yml
```

Pin `version` so builds are reproducible. Chart output then flows through the rest of the build, so you can patch it with `patches` and `images`.

## Checked

2026-11-03. Confirmed against: the helmCharts reference page and the built-ins page (HelmChartInflationGenerator).
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
