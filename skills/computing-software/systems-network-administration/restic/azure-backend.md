---
id: computing-software.systems-network-administration.restic.azure-backend
name: azure-backend
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, azure, blob-storage, backend, access-tier, managed-identity]
level: practitioner
status: docs-checked
description: "Back up to Azure Blob Storage with account keys, SAS tokens, az login or managed identity, plus connections and access-tier options."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Blob Storage backend

URL form: container then path, for example the root of container `foo`:

```
restic -r azure:foo:/ init
```

## Authentication

Set `AZURE_ACCOUNT_NAME` and then one of:

- `AZURE_ACCOUNT_KEY`
- `AZURE_ACCOUNT_SAS`
- an `az login` session whose identity has the "Storage Blob Data Contributor" role
- managed or workload identity, used automatically when restic runs on Azure

`AZURE_FORCE_CLI_CREDENTIAL=true` forces the Azure CLI credential. `AZURE_ENDPOINT_SUFFIX` overrides the default `core.windows.net`, for sovereign clouds.

## Options

- `-o azure.connections=10` raises the connection count; default 5.
- `-o azure.access-tier=Hot|Cool|Cold` sets the tier for newly written blobs.

```
restic -o azure.access-tier=Cool -r azure:foo:/ backup /path/to/data
```

The `az login` identity needs at least the Storage Blob Data Contributor role on the storage account. Access tier values are `Hot`, `Cool` or `Cold`; if unset, the default comes from the storage account.

## Checked

2026-11-03. Confirmed in the restic docs pages Preparing a new repository (Microsoft Azure Blob Storage section) and Scripting (environment variables): container-and-path URL form, `AZURE_ACCOUNT_NAME`/`AZURE_ACCOUNT_KEY`/`AZURE_ACCOUNT_SAS`, `az login` with Storage Blob Data Contributor, managed and workload identity, `AZURE_FORCE_CLI_CREDENTIAL`, `AZURE_ENDPOINT_SUFFIX` default `core.windows.net`, `azure.connections` default 5, `azure.access-tier` values. Removed: advice on SAS scoping and the snapshots smoke-test paragraph (not in the docs).

Method: documentation only; no commands were run.
