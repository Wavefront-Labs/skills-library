---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.deploying-pyroscope-with-helm
name: deploying-pyroscope-with-helm
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [pyroscope-helm, pyroscope-storage, profiling-ebpf, pyroscope, continuous-profiling]
level: practitioner
status: docs-checked
description: "Deploy Grafana Pyroscope on Kubernetes with Helm: single binary vs microservices values, which object storage backends exist, and how to verify the install."
sources: ["https://grafana.com/docs/pyroscope/latest/deploy-kubernetes/helm/", "https://grafana.com/docs/pyroscope/latest/configure-server/storage/", "https://grafana.com/docs/pyroscope/latest/configure-server/reference-configuration-parameters/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying Pyroscope with Helm

## Install
```bash
helm repo add grafana https://grafana.github.io/helm-charts
kubectl create ns pyroscope
# single binary
helm -n pyroscope install pyroscope grafana/pyroscope
# microservices: instances share one backend for storage and querying
curl -Lo values-micro-services.yaml https://raw.githubusercontent.com/grafana/pyroscope/main/operations/pyroscope/helm/pyroscope/values-micro-services.yaml
helm -n pyroscope install pyroscope grafana/pyroscope --values values-micro-services.yaml
```
Use a namespace of your choosing; the Pyroscope guide installs into a test namespace and adds Grafana alongside.

## Object storage
In the server configuration the storage `backend` supports `s3`, `gcs`, `azure`, `swift`, `filesystem` and `cos`
(`-storage.backend`), and the default is `filesystem`. Each backend has its own block (`s3`, `gcs`, `azure`,
`swift`, `filesystem`); read the reference configuration page for the fields of the block you use rather than
copying field names from memory. In the Helm chart, server configuration is passed through the chart values; check
the chart's values file for the exact key.

## Retention
The reference page documents v1-storage-only disk retention flags
(`-pyroscopedb.retention-policy-enforcement-interval`, `-pyroscopedb.retention-policy-disable`, and minimum
free-disk settings). For object-storage retention read the limits section of the same page for the setting your
version supports.

## Grafana
The Pyroscope Helm guide port-forwards the Grafana service it deploys (`kubectl port-forward` to port 3000) and adds
Pyroscope as a data source; follow that page for the connection steps.

## Checked
2026-11-01. Confirmed on the Helm guide (repo add URL, single vs microservices install, the values-micro-services
download, port-forward example) and the reference configuration page (backend list, default `filesystem`, v1
retention flags). Removed: S3 example with bucket and region, IRSA advice, `extraEnvFrom`, `limits.compactor_blocks_
retention_period` value, ingestion paths and ports, `multitenancy_enabled`, datasource type and URL, sizing hints and
the metric name used to verify.
Method: documentation only; no commands were run.
