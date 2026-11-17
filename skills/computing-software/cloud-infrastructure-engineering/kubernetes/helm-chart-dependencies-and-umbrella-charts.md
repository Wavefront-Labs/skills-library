---
id: computing-software.cloud-infrastructure-engineering.kubernetes.helm-chart-dependencies-and-umbrella-charts
name: helm-chart-dependencies-and-umbrella-charts
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, helm, chart-dependencies, umbrella-chart, subchart, library-chart, chart-lock]
level: practitioner
status: verified
description: "Compose Helm charts with dependencies: Chart.yaml entries, Chart.lock, conditions/tags/aliases, passing values to subcharts, import-values, library charts, and when umbrellas hurt."
sources: ["https://helm.sh/docs/helm/helm_dependency/", "https://helm.sh/docs/topics/charts/#chart-dependencies", "https://helm.sh/docs/chart_template_guide/subcharts_and_globals/", "https://helm.sh/docs/topics/library_charts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Helm chart dependencies and umbrella charts

## Declare
```yaml
# Chart.yaml
apiVersion: v2
name: shop
version: 2.3.0
dependencies:
- name: postgresql
  version: "16.x.x"
  repository: oci://registry-1.docker.io/bitnamicharts
  condition: postgresql.enabled
- name: redis
  version: "~20.1.0"
  repository: https://charts.example.com
  alias: cache
  tags: [backing-services]
- name: common
  version: "1.2.0"
  repository: file://../common            # local library chart
```
```bash
helm dependency update ./shop    # resolve ranges, write Chart.lock, download to charts/
helm dependency build ./shop     # reproducible: use Chart.lock exactly (CI)
                                 # fails with "lock file ... out of sync" if Chart.yaml changed since the lock
helm dependency list ./shop
```
Commit `Chart.lock`; decide whether to commit `charts/*.tgz` (vendoring helps air-gapped CI).

## Values flow
```yaml
# shop/values.yaml
postgresql:
  enabled: true
  auth: {database: shop}
cache:                     # alias name, not "redis"
  architecture: standalone
global:
  imageRegistry: registry.example.com
```
Subcharts see only their own section and `global`. To read a subchart value in the parent,
export it from the child (`exports:` in child values) and use `import-values` in the
dependency entry.

## Enable/disable
`condition` (a values path, first found wins) overrides `tags`. `--set tags.backing-services=false`
drops every dependency with that tag.

## Library charts
`type: library` charts only provide `define`d templates (`{{ include "common.labels" . }}`),
render nothing themselves (`helm install` and `helm template` of a library chart fail with `library charts are not installable`), and remove copy-paste across service charts.

## Umbrella chart trade-offs
Pros: one versioned bundle, one `helm install` for a whole environment.
Cons:
- One release = one blast radius; a failed hook rolls back everything.
- Everything upgrades together; independent service release cadence is lost.
- Release Secret holds the whole rendered manifest, and Secrets are capped at 1 MiB:
  big umbrellas fail with `Too long: must have at most 1048576 bytes`.
- Subchart name collisions and shared `fullnameOverride` confusion.
Prefer per-service releases orchestrated by Helmfile, Argo CD ApplicationSets or Flux for
large systems; use umbrellas for an app plus its tightly coupled backing services.

## Verify
```bash
helm lint ./shop --with-subcharts
helm template shop ./shop | grep -c '^kind:'       # expected object count
helm template shop ./shop --set postgresql.enabled=false | grep -c postgresql   # 0
```

## Checked
- Helm 3.15.2 with local `file://` subcharts (the Chart.yaml above with range versions, alias, condition, tags, import-values): `dependency list` shows `missing` then `ok`; `update` resolves `16.x.x` and `~20.1.0` to 16.4.2 and 20.1.7, writes `Chart.lock` and `charts/*.tgz`; `build` fails when Chart.yaml and the lock disagree; the alias name carries the values; `import-values` copied `exports.data`; a subchart sees its own section plus `global`; `condition` beats `tags` in both directions and `--set tags.x=false` drops tagged dependencies; the library helper rendered via `include`; `helm template shop | grep -c '^kind:'` and the `postgresql.enabled=false` count of 0 match. `oci://registry-1.docker.io/bitnamicharts/postgresql` version 16.4.2 pulls (latest is now 18.x). The Kubernetes Secret page states the 1MiB limit; the exact `Too long` error text was not reproduced.
