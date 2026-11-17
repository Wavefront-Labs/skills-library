---
id: computing-software.devops-ci-cd.helm.chart-hooks-overview
name: chart-hooks-overview
category: computing-software
field: devops-ci-cd
product: helm
tags: [hooks, pre-install, post-install, pre-upgrade, post-upgrade, pre-delete, post-delete, pre-rollback, post-rollback, lifecycle]
level: practitioner
status: docs-checked
description: "Helm hook lifecycle events and the helm.sh/hook annotation: pre/post install, upgrade, delete, rollback and test."
sources:
  - "https://helm.sh/docs/topics/charts_hooks/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Hooks are templates in `templates/` carrying the annotation `helm.sh/hook`. Helm runs them at defined points of a release lifecycle.

Supported values:

- `pre-install`: after templates render, before any resource is created.
- `post-install`: after all resources are loaded.
- `pre-delete`: on a delete request, before any resource is deleted.
- `post-delete`: after all release resources are deleted.
- `pre-upgrade`: on an upgrade request, after rendering, before any resource is updated.
- `post-upgrade`: after all resources are upgraded.
- `pre-rollback` / `post-rollback`: around a rollback request.
- `test`: run by `helm test`.

A hook can list several events, comma-separated: `"helm.sh/hook": post-install,post-upgrade`.

```yaml
metadata:
  annotations:
    "helm.sh/hook": pre-install
```

Hooks are usually Jobs or Pods. Helm waits for a hook to become ready (a Job to complete) before continuing, so a failing hook fails the release operation. The hook resource is not tracked or managed as part of the release; once Helm verifies it, Helm leaves it alone, so deleting the release does not delete it unless a delete policy says so.

Other facts from the hooks guide:

- A resource can implement several hooks and many resources can implement the same one. Hooks declared by subcharts are also evaluated, and a top-level chart cannot disable them.
- Before `pre-install` hooks run, CRDs in `crds/` are installed. The old `crd-install` hook was removed in Helm 3.
- With `--wait`, Helm waits for all resources to be ready before running `post-install`.
- For kinds other than Job and Pod, the hook is "Ready" as soon as Kubernetes marks the resource loaded.
- `--no-hooks` on `helm install` (prevent hooks from running) and `helm upgrade` (disable pre/post upgrade hooks) skips them.
- To destroy hook resources, add a `helm.sh/hook-delete-policy` annotation or set a Job TTL; `helm uninstall` does not remove them.

## Checked

2026-11-08. Read the Chart Hooks page in full. Removed unsupported claims (helm template renders hooks, helm get hooks); added subchart hooks, crds ordering, crd-install removal, --wait and Ready semantics.

Method: documentation only; no commands were run.
