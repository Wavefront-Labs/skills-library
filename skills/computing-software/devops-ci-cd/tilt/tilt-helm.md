---
id: computing-software.devops-ci-cd.tilt.tilt-helm
name: tilt-helm
category: computing-software
field: devops-ci-cd
product: tilt
tags: [helm, tilt, helm-charts, tiltfile]
level: practitioner
status: docs-checked
description: "Deploy Helm charts with Tilt: helm_resource for existing charts, the helm() built-in for charts you iterate on, helm_remote, and sub-chart ignores."
sources:
  - "https://docs.tilt.dev/helm.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Helm with Tilt

Goal: install off-the-shelf charts, or iterate on your own chart, from a Tiltfile.

## Install an existing chart

Use the `helm_resource` extension. On `tilt up` it runs `helm install`, reports the objects it installed, and shows logs, events and health checks in the Tilt UI.

```
load('ext://helm_resource', 'helm_resource', 'helm_repo')
helm_repo('bitnami', 'https://charts.bitnami.com/bitnami')
helm_resource('mysql', 'bitnami/mysql', resource_deps=['bitnami'])
```

## Iterate on your own chart

`helm()` runs `helm template` on a chart directory and returns YAML for `k8s_yaml`. Editing files in the chart directory redeploys automatically.

```python
yaml = helm(
  'path/to/chart/dir',
  name='release-name',
  namespace='my-namespace',
  values=['./path/to/chart/dir/values-dev.yaml'],
  set=['service.port=1234', 'ingress.enabled=true']
  )
k8s_yaml(yaml)
```

Tilt can validate the YAML, split it into per-server resources and auto-inject locally built images. `helm()` skips chart hooks and is offline-only; for a remote chart use `helm_remote`:

```python
load('ext://helm_remote', 'helm_remote')
helm_remote('mysql',
            repo_name='bitnami',
            repo_url='https://charts.bitnami.com/bitnami')
```

## Sub-charts

Run `helm dep update` outside Tilt, then add a `.tiltignore` with `**/charts` and `**/tmpcharts` (or the narrower `path/to/your/chart/charts` and `path/to/your/chart/tmpcharts`). Helm touches those directories, and this stops Tiltfile reloads.

## Shelling out

`local()` runs shell commands and `watch_file()` reloads the Tiltfile on change:

```
k8s_yaml(local('helm template -f ./values.yaml path/to/chart/dir'))
watch_file('path/to/chart/dir')
watch_file('values.yaml')
```

The same pattern wraps helmfile:

```
def helmfile(file):
  watch_file(file)
  return local("helmfile -f %s template" % file)
k8s_yaml(helmfile("k8s/staging/helmfile.yaml"))
```

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Helm page in full (existing charts, `helm()` and its options, pros and cons, remote charts, sub-charts, Advanced Helm recipes). Confirmed the `helm_resource` and `helm_remote` examples, the `helm()` options, the chart-hooks and offline-only limits, the `.tiltignore` patterns and the `local()` and `watch_file()` recipes including helmfile. Not opened: the helm_resource and helm_remote READMEs and the demo repositories. Nothing removed. 

Method: documentation only; no commands were run.
