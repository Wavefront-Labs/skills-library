---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-hub-model-registry-catalog
name: kubeflow-hub-model-registry-catalog
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [kubeflow-hub, model-registry, model-catalog, model-lineage]
level: intro
status: docs-checked
description: "Kubeflow Hub (formerly Model Registry): the registry metadata store, the read-only Model Catalog with YAML and Hugging Face sources, and the lifecycle use cases."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/hub/overview.md", "https://github.com/kubeflow/website/blob/master/content/en/docs/components/hub/reference/architecture.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hub model registry catalog

Kubeflow Hub (formerly Model Registry) manages the ML model lifecycle with two parts.

**Model Registry**: a central metadata index where teams register, version and track models, model versions and artifacts, bridging experimentation and production. It supports Create, Verify, Package, Release, Deploy and Monitor stages, with metrics, lineage and approval status per version.

**Model Catalog**: a read-only discovery service that federates model metadata from external sources behind one REST API. Source types: static YAML catalogs and Hugging Face Hub (organization-scoped and include or exclude patterns). Metadata includes description, provider, tasks, languages, license and custom properties such as `model_type`; you can filter by those. It stores no weights or artifacts, only metadata and references, and a found model can be registered into a Registry.

Architecture: the registry is a passive metadata repository, not a control plane; it performs no orchestration of Kubernetes components. It stores metadata in a backend RDBMS using an ER model inspired by Google ML-Metadata, exposes an OpenAPI REST server (register and version models, get a catalog of models, manage deployment status), and ships Python and Go clients.

Documented personas: a data scientist tracking training runs and metrics, an MLOps engineer fetching the approved latest version to configure deployment, and an analyst auditing lineage and drift.

## Checked

Confirmed the Registry and Catalog split, the lifecycle stages, the YAML and Hugging Face source types, the metadata-only behaviour, the passive-repository note, the ML-Metadata-inspired RDBMS model and the personas. Reworded the REST API capability list to the page's wording.

Method: docs-checked 2026-11-09 against the raw kubeflow/website Hub overview.md and reference/architecture.md pages, read in full.
