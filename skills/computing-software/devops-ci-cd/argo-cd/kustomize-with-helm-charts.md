---
id: computing-software.devops-ci-cd.argo-cd.kustomize-with-helm-charts
name: kustomize-with-helm-charts
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, kustomize-enable-helm, kustomize-helm-charts, helmcharts-inflation]
level: advanced
status: docs-checked
description: "Inflate Helm charts inside Kustomize in Argo CD with helmCharts and --enable-helm, patch the output, and handle private chart repos and caching limits."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/kustomize/#kustomizing-helm-charts", "https://kubectl.docs.kubernetes.io/references/kustomize/builtins/#_helmchartinflationgenerator_", "https://github.com/kubernetes-sigs/kustomize/blob/master/examples/chart.md", "https://github.com/kubernetes-sigs/kustomize/blob/master/api/types/helmchartargs.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kustomize with Helm charts (`--enable-helm`)

## 1. Enable
```yaml
# argocd-cm
data:
  kustomize.buildOptions: --enable-helm
```

## 2. kustomization.yaml
```yaml
helmCharts:
  - name: external-dns
    repo: https://charts.example.com/
    version: <chart-version>
    releaseName: external-dns
    namespace: external-dns
    valuesFile: values.yaml
    valuesInline:
      provider: { name: aws }
    includeCRDs: true
patches:
  - target: { kind: Deployment, name: external-dns }
    patch: |-
      - op: add
        path: /spec/template/spec/priorityClassName
        value: system-cluster-critical
```
Why: patch anything the chart does not expose as a value, add resources next to the chart, and use overlays per environment.

## 3. Limits
- kustomize runs the `helm` command-line program in a subprocess to inflate the chart, so `helm`
  must be available where `kustomize build` runs (for Argo CD, the repo-server).
- **Vendoring:** kustomize looks for the chart at `{kustomizationRoot}/{chartHome}/<name>` (the
  `chartHome` field) and, if it is there at build time, uses it as found without checking versions
  or pulling; otherwise it pulls the chart at the given `version`. Committing the chart into Git
  therefore avoids network pulls at render time.
- Credentials for a private chart repository are not covered by the Argo CD or kustomize docs
  read for this check; vendoring the chart is the way to avoid the question.
- `skipHooks: true` makes kustomize pass `--no-hooks` to `helm template`.

## 4. Local parity
`kustomize build --enable-helm overlays/prod` must produce what Argo CD renders — run it in CI.

## Verify
- [ ] `argocd app manifests` contains the chart resources with your patch applied.

## Checked

2026-10-25, against the Argo CD Kustomize user guide, kustomize `examples/chart.md` and `api/types/helmchartargs.go` (master). Confirmed: `kustomize.buildOptions: --enable-helm` in `argocd-cm` (global for all Kustomize apps), `helmCharts` fields (`name`, `repo`, `version`, `releaseName`, `namespace`, `valuesFile`, `valuesInline`, `includeCRDs`, `chartHome`, `skipHooks`), helm run as a subprocess, chart vendoring via `chartHome`. Removed as unconfirmed: the claim that Argo CD repo credentials are not passed to helm, the per-render caching claim, the 'hooks become plain resources' claim, and the pinned external-dns chart version.

Method: documentation only; no commands were run.
