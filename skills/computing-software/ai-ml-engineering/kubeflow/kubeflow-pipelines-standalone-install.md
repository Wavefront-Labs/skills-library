---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-standalone-install
name: kubeflow-pipelines-standalone-install
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [standalone-install, kustomize-install, kubernetes-native-api, pipeline-version, cert-manager-install]
level: practitioner
status: docs-checked
description: "Install Kubeflow Pipelines standalone with kustomize: cluster-scoped resources, the dev or platform-agnostic overlay, Kubernetes native API mode with cert-manager, and TLS."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/operator-guides/installation/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines standalone install

KFP can run standalone instead of inside the Community Distribution. You should know Kubernetes, kubectl and kustomize. The documentation says the version placeholder resolves to the latest release automatically.

Standard install:

```bash
export PIPELINE_VERSION=<release>
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
```

The `env/dev` flavor is for first, non-production experiments; the documentation points to the Community Distribution for production-ready environments.

Kubernetes native API mode stores pipeline definitions as Kubernetes custom resources instead of in an external database. Install cert-manager (the docs use v1.18.2), wait for its pods, then apply `env/cert-manager/platform-agnostic-k8s-native`. A migration script exists for upgrading from non-native deployments.

Pod-to-pod TLS: the API server serves TLS and connecting deployments mount CA certificates. The `platform-agnostic-standalone-tls` overlay holds the manifests, and a KinD target in the backend Makefile can deploy it.

For the full Kubeflow Community Distribution use the kubeflow/manifests repository instead (install just KFP, or the single-command install).

## Checked

Confirmed the dev-flavor commands, the Kubernetes native API mode steps with cert-manager v1.18.2, the migration script note and the pod-to-pod TLS paragraph. Removed the platform-agnostic MySQL remark and the MySQL claim for the TLS overlay because the page does not state them.

Method: docs-checked 2026-11-09 against the raw kubeflow/website pipelines operator-guides installation _index.md page, read in full.
