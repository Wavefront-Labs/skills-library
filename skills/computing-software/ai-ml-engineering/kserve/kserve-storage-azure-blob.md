---
id: computing-software.ai-ml-engineering.kserve.kserve-storage-azure-blob
name: kserve-storage-azure-blob
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [azure, azure-blob, az-client-id, az-client-secret, az-subscription-id, az-tenant-id, azure-storage-access-key, azure-max-file-concurrency, azure-max-chunk-concurrency, sas-token, service-principal]
level: practitioner
status: docs-checked
description: "Serve models from Azure Blob Storage: anonymous or service principal (AZ_* keys) or SAS/access key Secret, and AZURE_MAX_FILE_CONCURRENCY / AZURE_MAX_CHUNK_CONCURRENCY tuning."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/storage/providers/azure.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Azure Blob model storage

URI format: `https://{$STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{$CONTAINER}/{$PATH}`. Public blobs download anonymously by default.

Private blobs use an Azure service principal with the Storage Blob Data Owner role on the blob (KServe must list the contents at the blob path to filter what to download), created with `az ad sp create-for-rbac --name model-store-sp --role "Storage Blob Data Owner" --scopes <storage-account-resource-id>`).

```yaml
apiVersion: v1
kind: Secret
metadata: {name: azcreds}
type: Opaque
stringData:
  AZ_CLIENT_ID: xxxxx
  AZ_CLIENT_SECRET: xxxxx
  AZ_SUBSCRIPTION_ID: xxxxx
  AZ_TENANT_ID: xxxxx
```

A SAS token can be used instead: put `AZURE_STORAGE_ACCESS_KEY: xxxxx` in an Opaque Secret. Use `stringData` for raw text or `data` for base64.

Attach `azcreds` to a ServiceAccount `secrets:` list and set `spec.predictor.serviceAccountName`.

## Download tuning
On the `ClusterStorageContainer` container env (defaults shown):

```yaml
- name: AZURE_MAX_FILE_CONCURRENCY
  value: 4        # files downloaded in parallel
- name: AZURE_MAX_CHUNK_CONCURRENCY
  value: 4        # parallelism within each file
```

Each download has a buffer of 8MiB.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website Azure storage page: URI format, anonymous default, service principal role and command, Secret keys, SAS token variant, ServiceAccount wiring, and both concurrency variables with defaults of 4. Removed the claim that memory scales with the product of the settings, which the page does not state.
