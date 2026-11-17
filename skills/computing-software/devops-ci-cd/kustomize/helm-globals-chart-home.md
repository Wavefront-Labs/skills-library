---
id: computing-software.devops-ci-cd.kustomize.helm-globals-chart-home
name: helm-globals-chart-home
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [helmglobals, charthome, confighome, helm]
level: advanced
status: docs-checked
description: "helmGlobals sets chartHome and configHome for all helmCharts entries and controls whether kustomize pulls a chart or uses a vendored copy."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/builtins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`helmGlobals` stores settings that affect all entries in `helmCharts`.

```yaml
helmGlobals:
  chartHome: my-charts-dir
```

- `chartHome`: a file path, relative to the kustomization root, to a directory with a subdirectory per chart. Default `charts`. Kustomize looks for the minecraft chart at `{kustomizationRoot}/{chartHome}/minecraft`.
- `configHome`: the value passed to helm via the `HELM_CONFIG_HOME` environment variable. Kustomize neither reads nor writes it. If omitted, `{tmpDir}/helm` is used, in a temporary directory kustomize creates.

Pull behavior: if the chart is already in `chartHome` at build time, kustomize uses it as found and does not check version numbers or dates. If it is absent, kustomize tries to pull it with the version in the kustomization and puts it there. To suppress the pull attempt, make sure the chart is already present.

Practical use:

- Vendor charts into `chartHome` and commit them for offline or hermetic CI builds.
- After bumping `version`, delete the old chart directory, otherwise the stale copy is used silently.
- Add the downloaded chart directory to `.gitignore` if you prefer pulling at build time.

The same fields are available when running through the `generators` field as a `HelmChartInflationGenerator` with `apiVersion: builtin`.

## Checked

2026-11-08: confirmed against the Kustomize Built-Ins page, read in full (helmGlobals chartHome and configHome, default `charts`, pull behaviour, HelmChartInflationGenerator example). The practical-use bullets are advice drawn from the stated pull behaviour, not separate documented claims.

Method: documentation only; no commands were run.
