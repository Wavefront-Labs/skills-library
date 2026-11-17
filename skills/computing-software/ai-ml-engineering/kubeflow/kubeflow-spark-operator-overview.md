---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-spark-operator-overview
name: kubeflow-spark-operator-overview
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [spark-operator, sparkapplication, spark-submit, cron-scheduling]
level: intro
status: docs-checked
description: "Kubeflow Spark Operator: running Spark applications as SparkApplication custom resources with cron scheduling, restart policies, a mutating webhook and Prometheus metrics."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/spark-operator/overview.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Spark operator overview

The Kubernetes Operator for Apache Spark (Kubeflow Spark Operator) lets you specify and run Spark applications as idiomatically as other Kubernetes workloads. It uses custom resources to specify, run and report status.

Benefits listed by the documentation:
- **Declarative management**: describe applications with a `SparkApplication` custom resource in YAML.
- **Automated execution**: the operator performs `spark-submit` on your behalf whenever a valid application manifest is created or updated.
- **Native cron scheduling**: built-in support for running recurring Spark jobs on a schedule (the project documents a scheduled application guide).
- **Pod customization**: a mutating admission webhook applies customizations beyond Spark's native capabilities, such as mounting ConfigMaps and volumes or setting pod affinity and anti-affinity.
- **Failure handling**: configurable restart policies, automatic re-submission when the spec is updated, and submission retries with configurable linear back-off.
- **Prometheus observability**: application, driver and executor metrics can be exported to Prometheus.

The Kubeflow site page is only an overview. Deployment, the guide to writing a SparkApplication manifest, the API reference and customization options live on the Spark Operator project site (spark.kubeflow.org), which is the next stop for installing and writing manifests.

## Checked

Confirmed each listed benefit and the pointers to the Spark Operator project site. Nothing removed.

Method: docs-checked 2026-11-09 against the raw kubeflow/website spark-operator overview.md page, read in full.
