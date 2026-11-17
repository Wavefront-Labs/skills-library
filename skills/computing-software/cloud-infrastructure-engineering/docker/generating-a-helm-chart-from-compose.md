---
id: computing-software.cloud-infrastructure-engineering.docker.generating-a-helm-chart-from-compose
name: generating-a-helm-chart-from-compose
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-to-helm, kompose-chart, kompose, katenary, helm, compose-to-kubernetes, values-yaml, helm-lint]
level: advanced
status: docs-checked
description: "Turn a Compose file into a maintainable Helm chart: kompose --chart output and its limits, katenary for values-driven charts, parameterising by hand, and validating the result."
sources: ["https://kompose.io/user-guide/", "https://github.com/kubernetes/kompose/blob/main/cmd/convert.go", "https://github.com/docker/compose/blob/main/docs/reference/compose_config.md", "https://github.com/katenary/katenary/blob/master/doc/docs/labels.md", "https://helm.sh/docs/helm/helm_lint/", "https://helm.sh/docs/helm/helm_install/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating a Helm chart from Compose

**Goal:** a Helm chart for a stack that today lives in `compose.yaml`, with real
`values.yaml` knobs (image tags, replicas, hosts, resources) rather than frozen manifests.

## Step 0: flatten the Compose input
```bash
docker compose -f compose.yaml -f compose.prod.yaml config > resolved.yaml
```
`docker compose config` merges the `-f` files, resolves variables and expands short syntax into
the canonical format, which gives converters one plain input instead of overrides and `${VAR}`.

## Option 1: kompose --chart (skeleton)
```bash
kompose convert -f resolved.yaml --chart -o chart/          # -c is the short form
```
`--chart`/`-c` creates a Helm chart for the converted objects, but the flag is hidden from
`kompose convert --help` in the current source. Inspect the generated chart: do not assume
it exposes useful `values.yaml` knobs, and treat it as a starting point.

Steer the output with Compose labels before converting:
```yaml
services:
  api:
    labels:
      kompose.service.type: clusterip
      kompose.service.expose: api.example.com     # Ingress
      kompose.controller.type: deployment
  db:
    labels:
      kompose.controller.type: statefulset
      kompose.volume.size: 20Gi
```

## Option 2: katenary (values-driven)
katenary converts Compose to a Helm chart (default output directory `chart`), configured with
`katenary.v3/*` labels:
```bash
katenary convert -c resolved.yaml -o chart/
```
`-c` selects the compose file (repeatable) and `-o` the output directory. Label examples:
`katenary.v3/ingress` (an object with `hostname` and `port`), `katenary.v3/configmap-files`,
`katenary.v3/map-env`, `katenary.v3/values`. The label prefix carries a version, so check the
label reference for the version you install.

## Parameterise by hand (whichever tool you start from)
Move these into `values.yaml` at minimum:
```yaml
api:
  image: { repository: ghcr.io/org/api, tag: "1.4.2", pullPolicy: IfNotPresent }
  replicas: 2
  resources: { requests: { cpu: 100m, memory: 256Mi }, limits: { memory: 512Mi } }
  ingress: { enabled: true, host: api.example.com, tlsSecret: api-tls }
  env: { LOG_LEVEL: info }
```
and template them (`{{ .Values.api.image.repository }}:{{ .Values.api.image.tag | default .Chart.AppVersion }}`).
Also review what converters tend to miss: readiness/liveness probes (Compose healthchecks
map poorly), `resources.requests`, secrets (use external secrets, not `env_file` → ConfigMap),
bind mounts (→ PVCs or ConfigMaps), `depends_on` (→ probes/init containers).
Databases often become a dependency chart instead of a converted StatefulSet:
```yaml
# Chart.yaml
dependencies:
  - name: postgresql
    version: "<version-or-range>"
    repository: oci://registry.example.com/charts
```

## Validate
```bash
helm lint chart/shop
helm template shop chart/shop -f values-prod.yaml
helm install shop chart/shop --dry-run=server -n shop --create-namespace
```
After this, the chart is the source of truth; stop regenerating it from Compose or manual
fixes get overwritten. Keep Compose for local dev only.

## Verify
```bash
helm install shop chart/shop -n shop --create-namespace --wait --timeout 5m
kubectl -n shop get deploy,sts,svc,ingress
```

## Checked

2026-10-25, against kompose user guide and `cmd/convert.go` (main), katenary usage, README and label reference, the Docker Compose `compose config` reference, and Helm lint/install references. Confirmed: `docker compose config` behaviour, kompose `--chart/-c` flag (hidden) and `-o`, the `kompose.service.type`, `kompose.service.expose`, `kompose.controller.type` (statefulset) and `kompose.volume.size` labels, `katenary convert -c/-o` and the listed `katenary.v3/*` labels, `helm lint` and `--dry-run=server`. Removed: the claim of a generated chart layout and 'no values.yaml', the kubeconform pipeline, the Bitnami dependency pin.

Method: documentation only; no commands were run.
