---
id: computing-software.ai-ml-engineering.seldon-core-2.installation-modes-and-dependency-versions
name: installation-modes-and-dependency-versions
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, installation, dependencies, supported-versions, kubernetes, envoy, rclone, kafka, prometheus, grafana, prometheus-adapter, opentelemetry-collector, docker-compose, kind]
level: practitioner
status: docs-checked
description: "Pick a Seldon Core 2 install mode (Docker Compose, Kind, managed or on-prem Kubernetes) and check supported versions for Kubernetes, Envoy, Rclone, Kafka and optional parts."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/installation/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install modes and dependency versions

## Modes
- Local: Docker Compose (lightweight, no Kubernetes needed) or Kind (Kubernetes in Docker, realistic for Kubernetes-native features).
- Production: managed Kubernetes (GKE, EKS, AKS) or on-premises clusters such as OpenShift or custom setups for compliance or data sovereignty needs.

## Supported component versions
| Component | Min | Max | Notes |
| --- | --- | --- | --- |
| Kubernetes | 1.27 | 1.33.0 | Required |
| Envoy | 1.32.2 | 1.32.2 | Required, included in the Core 2 images |
| Rclone | 1.68.2 | 1.69.0 | Required, included in the Core 2 images |
| Kafka | 3.4 | 3.8 | Recommended; only required for dataflow Pipelines |
| Prometheus | 2.0 | 2.x | Optional |
| Grafana | 10.0 | no hard limit | Optional |
| Prometheus-adapter | 0.12 | 0.12 | Optional |
| OpenTelemetry Collector | 0.68 | no hard limit | Optional |

Envoy and Rclone ship inside the Seldon images, so you do not install them separately, but you must respect the configuration options those versions support.

Kafka is only needed to operate Pipelines. If you do not need them, avoid installing `seldon-modelgateway`, `seldon-pipelinegateway` and `seldon-dataflow-engine`.

## Charts
The chart set is `seldon-core-v2-crds`, `seldon-core-v2-setup`, `seldon-core-v2-runtime` and `seldon-core-v2-servers`; see the Helm installation skill for the commands.

## Checked

2026-11-04. Confirmed against installation/README.md (Seldon Core 2 docs, v2 branch): modes and the supported-version table. Removed or corrected: nothing.

Method: documentation only; no commands were run.
