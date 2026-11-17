---
id: computing-software.cloud-infrastructure-engineering.fluentd.kubernetes-daemonset
name: kubernetes-daemonset
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, kubernetes, daemonset, elasticsearch, fluentd-kubernetes-daemonset, environment-variables]
level: practitioner
status: docs-checked
description: "Deploy Fluentd on Kubernetes as a DaemonSet from fluent/fluentd-kubernetes-daemonset and configure the Elasticsearch output with FLUENT_ELASTICSEARCH variables."
sources:
  - https://docs.fluentd.org/container-deployment/kubernetes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd on Kubernetes
Run one Fluentd pod per node with a DaemonSet to collect node and pod logs. The project repository is `fluent/fluentd-kubernetes-daemonset`; clone it, which holds presets for Alpine and Debian images with popular outputs.

For Elasticsearch, edit `fluentd-daemonset-elasticsearch.yaml` (image `quay.io/fluent/fluentd-kubernetes-daemonset`, namespace `kube-system`) before deploying. Environment variables:

| Variable | Meaning | Default |
| --- | --- | --- |
| `FLUENT_ELASTICSEARCH_HOST` | host name or IP | `elasticsearch-logging` |
| `FLUENT_ELASTICSEARCH_PORT` | TCP port | 9200 |
| `FLUENT_ELASTICSEARCH_SSL_VERIFY` | verify certificates | `true` |
| `FLUENT_ELASTICSEARCH_SSL_VERSION` | TLS version | `TLSv1_2` |

Defaults assume an Elasticsearch pod named `elasticsearch-logging` exists in the cluster.

The page introduces the destination question first: choose where logs go, then configure the DaemonSet for that destination.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/container-deployment/kubernetes and confirmed: repository, preset file, image, FLUENT_ELASTICSEARCH variables and defaults. Removed or reworded: the unsupported "pick or build the preset" wording.

Method: documentation only; no commands were run.
