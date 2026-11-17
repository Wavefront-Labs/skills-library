---
id: computing-software.ai-ml-engineering.kserve.kserve-storage-overview-initializer
name: kserve-storage-overview-initializer
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [storage-initializer, storageuri, storageuris, model-storage, init-container, storage-providers, mntmodels, clusterstoragecontainer]
level: practitioner
status: docs-checked
description: "How KServe fetches model artifacts: storageUri vs storageUris, supported providers (S3, GCS, Azure, URI, Git, PVC, Hugging Face, ModelScope, OCI), storage initializer."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/storage/overview.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# KServe model storage overview

An InferenceService points at artifacts with `storageUri` (the traditional single-artifact field) or `storageUris` (the newer field for fetching artifacts from multiple locations with custom mount paths).

The **storage initializer** is an init container that downloads the model artifact from its source into a local directory the model server container can read. Its capabilities per the overview: downloading from different providers, authenticating to secured storage, custom certificates for secure connections, direct volume mounting with PVCs, and "modelcars" for serving from OCI images.

## Providers
| Group | Providers |
|---|---|
| Cloud storage | Amazon S3, Google Cloud Storage (GCS), Azure Blob Storage |
| Other | HTTP/HTTPS URI, Git, Persistent Volume Claims (PVC), Hugging Face hub, ModelScope hub, OCI images (Modelcars) |

Each provider has its own page (for the URI form, credentials and examples): see the sibling skills for GCS, HTTP URI, Git, PVC and multiple URIs.

## Authentication
- Service account credentials (for cloud storage providers).
- Access keys and secrets (for S3-compatible storage).
- Self-signed certificates, for storage systems with self-signed SSL certificates (see the CA bundle skill).
- Credentials are configured with Kubernetes Secrets.

## Customisation
- The `ClusterStorageContainer` CRD defines custom initialisation logic.
- Storage credentials are configured with Kubernetes secrets.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the KServe "Storage Options for Model Artifacts" overview page.
Removed as not stated there: the per-provider URI form table (hf://, oci://, azure URL), IAM role for service account, the per-URI-prefix behaviour of ClusterStorageContainer, global defaults under inferenceservice-config, and the Azure service principal detail.
