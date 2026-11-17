---
id: computing-software.cloud-infrastructure-engineering.azure.acr-oci-artifacts-with-oras-and-referrers
name: acr-oci-artifacts-with-oras-and-referrers
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, container-registry, oras, referrers-api, oci-artifacts, sbom, helm-oci]
level: practitioner
status: docs-checked
description: "Store non-image artifacts in ACR with ORAS: push/pull files, attach SBOMs and signatures as referrers, discover the graph, and push Helm charts as OCI."
sources: ["https://learn.microsoft.com/azure/container-registry/container-registry-manage-artifact", "https://oras.land/", "https://learn.microsoft.com/azure/container-registry/container-registry-helm-repos"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCI artifacts in ACR with ORAS

**Goal:** keep configs, SBOMs, signatures and charts next to the images they describe, with one auth model.

## Login
```bash
az acr login --name crcorp                     # docker credential store; oras reuses it
# or: TOKEN=$(az acr login --name crcorp --expose-token --query accessToken -o tsv)
#     oras login crcorp.azurecr.io --username 00000000-0000-0000-0000-000000000000 --password "$TOKEN"
```

## Push and pull arbitrary files
```bash
oras push crcorp.azurecr.io/configs/orders:v3 --artifact-type application/vnd.contoso.config.v1 \
  ./appsettings.json:application/json ./rules.yaml:application/yaml
oras pull crcorp.azurecr.io/configs/orders:v3 -o ./out
```

## Attach referrers to an image (supply chain)
```bash
IMAGE=crcorp.azurecr.io/orders@sha256:<digest>
oras attach $IMAGE --artifact-type application/spdx+json ./sbom.spdx.json
oras attach $IMAGE --artifact-type application/vnd.cncf.notary.signature ./sig.cose   # usually done by notation
oras discover $IMAGE -o tree
```
ORAS (v1.2.3 and later) stores attached referrers through the OCI referrers API; ACR supports it for most features except customer-managed-key registries, where ORAS falls back to the referrers tag schema. Attach to a **digest**, not a mutable tag. Referrers are untagged because they belong to their subject.

## Helm charts as OCI
```bash
helm package ./chart
helm push orders-1.8.0.tgz oci://crcorp.azurecr.io/helm
helm install orders oci://crcorp.azurecr.io/helm/orders --version 1.8.0
```

## Lifecycle
- Remove an artifact with `oras manifest delete <ref>`.
- Authentication is the same as for images (Entra identity, service principal or repository-scoped token); `helm registry login` also works for charts.

## Verify
- [ ] `oras discover -o tree` shows the SBOM and signature under the image digest; `helm pull oci://crcorp.azurecr.io/helm/orders --version 1.8.0` succeeds.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-management-docs `container-registry-manage-artifact` and `container-registry-helm-repos` (main branch).
- Confirmed: `oras push --artifact-type`, `oras attach --artifact-type`, `oras discover -o tree`, `oras manifest delete`; referrers API behaviour and the CMK-registry fallback; `helm push oci://`, `helm install oci:// --version`, `helm pull oci:// --version`, `helm registry login`.
- Removed as unconfirmed: that deleting a subject deletes its referrers, and the purge/retention guidance.
Method: documentation only; no commands were run.
