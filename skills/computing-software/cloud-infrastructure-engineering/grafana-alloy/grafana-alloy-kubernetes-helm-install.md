---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-kubernetes-helm-install
name: grafana-alloy-kubernetes-helm-install
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [helm, kubernetes, alloyconfigmap, configmapcreate, kustomize, configmapgenerator, configreloader]
level: intro
status: docs-checked
description: "Deploy Alloy on Kubernetes with the Helm chart, apply configs via values.yaml or a ConfigMap, avoid the Kustomize hash trap."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/set-up/install/kubernetes.md", "https://github.com/grafana/alloy/blob/main/docs/sources/configure/kubernetes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alloy on Kubernetes with Helm

```shell
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
kubectl create namespace alloy
helm install --namespace alloy alloy grafana/alloy
kubectl get pods --namespace alloy
```

## Applying configuration
Upgrade with `helm upgrade --namespace NAMESPACE RELEASE grafana/alloy -f values.yaml`. The config lives in a ConfigMap, set one of two ways.

Method 1, inline:
```yaml
alloy:
  configMap:
    content: |-
      logging {
        level  = "info"
        format = "logfmt"
      }
```

Method 2, separate ConfigMap:
```shell
kubectl create configmap --namespace alloy alloy-config "--from-file=config.alloy=./config.alloy"
```
```yaml
alloy:
  configMap:
    create: false
    name: alloy-config
    key: config.alloy
```

## Kustomize gotcha
A `configMapGenerator` appends a content hash to the ConfigMap name and patches references, forcing a rolling restart. Alloy startup can be slow (for example a large metrics WAL), so set `options: { disableNameSuffixHash: true }` and let the chart's sidecar reloader watch the ConfigMap and trigger a dynamic reload.

## Checked

2026-11-08. Read in full the raw Alloy docs pages behind both cited URLs (docs/sources/set-up/install/kubernetes.md and docs/sources/configure/kubernetes.md): install commands, helm upgrade, both configuration methods, and the Kustomize considerations. Removed the `controller.type: statefulset` advice, which neither page states.

Method: documentation only; no commands were run.
