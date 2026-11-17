---
id: computing-software.cloud-infrastructure-engineering.azure.container-registry-tasks-and-image-security
name: container-registry-tasks-and-image-security
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, container-registry, acr, acr-tasks, image-scanning, geo-replication, acr-premium, private-endpoint, acr-pull, acr-push, managed-identity, admin-user, content-trust, image-signing, notation, retention-policy, acr-purge, soft-delete, artifact-cache, cache-rules, quarantine, acr-build, oci-artifacts, helm-oci, dedicated-data-endpoints, zone-redundancy]
level: practitioner
status: docs-checked
description: "Run ACR as the single image source: Premium geo-replication, identity-only auth, private endpoint, ACR Tasks builds, cache rules, purge/retention, Notation signing and Defender scanning."
sources: ["https://learn.microsoft.com/azure/container-registry/container-registry-skus", "https://learn.microsoft.com/azure/container-registry/container-registry-tasks-overview", "https://learn.microsoft.com/azure/container-registry/artifact-cache-cli", "https://learn.microsoft.com/azure/container-registry/container-registry-auto-purge", "https://learn.microsoft.com/azure/container-registry/container-registry-retention-policy", "https://learn.microsoft.com/azure/container-registry/container-registry-soft-delete-policy", "https://learn.microsoft.com/azure/container-registry/container-registry-rbac-abac-repository-permissions", "https://learn.microsoft.com/azure/container-registry/container-registry-tutorial-sign-build-push", "https://learn.microsoft.com/azure/container-registry/scan-images-defender"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Container Registry — private, replicated, identity-only, self-cleaning

**Goal:** every image your clusters run comes from ACR, pushed by a pipeline identity,
scanned, signed, replicated close to the consumers, and old tags garbage-collected.

## 1. Create
```bash
az acr create -n myacr -g rg-platform --sku Premium --admin-enabled false \
  --public-network-enabled false --allow-trusted-services true
az acr replication create -r myacr -l ukwest
az acr update -n myacr --data-endpoint-enabled true      # dedicated data endpoints (firewall-friendly FQDNs)
az network private-endpoint create ... --group-id registry --private-connection-resource-id <acr-id>   # zone privatelink.azurecr.io
```
- **Basic/Standard/Premium**: all SKUs have zone redundancy by default in supported regions; Premium adds
  geo-replication, private link with private endpoints, and higher API concurrency and bandwidth. Retention policy
  for untagged manifests is Premium and preview.
- Geo-replication = one registry name, requests routed to a healthy replica, storage billed per replica.
  See `acr-geo-replication-and-zone-redundancy` for routing and consistency behaviour.
- Names are global DNS (`myacr.azurecr.io`); with private endpoints you need the
  `privatelink.azurecr.io` zone with **two records per region** (`myacr` and `myacr.<region>.data`).
- Firewall exceptions when public access must stay: `az acr network-rule add --ip-address`; for Azure services use a private endpoint or trusted services access (`--allow-trusted-services`).

## 2. Authentication (no passwords)
| Client | How |
|---|---|
| AKS | `az aks update --attach-acr myacr` (grants kubelet identity *AcrPull*) |
| ACI / Container Apps / App Service / Functions | managed identity with *AcrPull* (the flag name differs per service; see that service's documentation) |
| Pipelines (Azure Pipelines, GitHub) | workload identity service connection → `az acr login -n myacr` (token, no secret) — role *AcrPush* |
| Humans | `az acr login -n myacr` (Entra) with *AcrPull* / *AcrPush* / *AcrDelete* / *AcrImageSigner* |
| Non-Azure tools that insist on a password | **scoped tokens** (`az acr token create --scope-map`) with expiry — never the admin user |
Keep `--admin-enabled false`.
Repository-scoped access: scope maps and tokens, or ABAC repository permissions (role assignment permissions mode
**RBAC Registry + ABAC Repository Permissions**). In an ABAC-enabled registry the legacy roles AcrPull, AcrPush and
AcrDelete are not honored, so assign the ABAC-enabled roles first (for example Container Registry Repository Reader
for pulls) before switching modes, or existing identities lose access.

## 3. ACR Tasks
```bash
az acr build -r myacr -t api:{{.Run.ID}} -t api:1.4.0 -f Dockerfile .     # cloud build, no local Docker, pushes result
az acr task create -r myacr -n build-api --context https://github.com/org/api.git#main \
  --file Dockerfile --image api:{{.Run.ID}} --git-access-token <PAT> --commit-trigger-enabled true \
  --base-image-trigger-enabled true          # rebuild when the base image updates in ACR/MCR
az acr task run -r myacr -n build-api; az acr task logs -r myacr
```
Multi-step tasks (`acr-task.yaml`: build → test → push → `cmd` to run a scanner) and
scheduled tasks (`--schedule "0 2 * * *"` for a nightly rebuild + purge). Agent pools
(`az acr agentpool`) put the build inside your VNet for private sources. `--platform` selects the target
(for example `linux/arm/v7` or `windows`).

## 4. Caching upstreams and OCI artifacts
- **Cache rules**: `az acr cache create -r myacr -n dockerhub --source-repo docker.io/library/* --target-repo dockerhub/* --cred-set dockerhub`
  — pull-through cache; cached images are then pulled as `myacr.azurecr.io/dockerhub/nginx`. Short options are `-s` (source), `-t` (target) and `-c` (credential set).
- Helm charts as OCI (`helm push chart.tgz oci://myacr.azurecr.io/helm`), SBOMs/signatures
  as referrers (`oras attach`) — one registry for images and OCI artefacts.

## 5. Cleanup and safety
- Purge: `az acr run -r myacr --cmd "acr purge --filter 'api:.*' --ago 30d --untagged --keep 10" /dev/null`
  on a scheduled task; **retention policy** (`az acr config retention update -r myacr --status enabled --days 7 --type UntaggedManifests`, Premium, preview) for untagged manifests.
- **Soft delete** (`az acr config soft-delete update -r myacr --days 7 --status enabled`, preview) to recover deleted artifacts; the default retention is 7 days, configurable from 1 to 90.
- Lock release images: `az acr repository update --name myacr --image api:1.4.0 --write-enabled false --delete-enabled false`.
- Sign: Notation + Key Vault (`notation sign --plugin azure-kv --id <key-id> myacr.azurecr.io/api@sha256:...`);
  verify in AKS with Ratify and Azure Policy or at deploy time in the pipeline (`notation verify`). Docker Content Trust is retiring in ACR on March 31, 2028; move to Notary Project signing. The signing identity needs Key Vault Crypto User.
- Scanning: Microsoft Defender for Cloud scans images that are pushed, imported, or pulled within the last 30 days; gate releases on its findings.
- Diagnostic logs `ContainerRegistryLoginEvents` and `ContainerRegistryRepositoryEvents` → Log Analytics for who pushed what.

## Gotchas
- Private endpoint + geo-replication: each replica adds a regional dedicated data endpoint that needs a private IP and DNS record in every VNet with a private endpoint (the subnet must have spare addresses).
- `az acr build` uploads your build context; use a `.dockerignore` to keep it small.
- `attach-acr` from another subscription/tenant needs explicit *AcrPull* on the kubelet identity; cross-tenant needs a token or federated identity.
- Tags are mutable: deploy by **digest** (`image@sha256:`) in production manifests; `acr purge --untagged` deletes manifests that have no tags, so know your retention before enabling it.
- Registries rate-limit API requests per SKU and return `429 Too Many Requests` with `Retry-After`; Premium has higher limits, which are best-effort and not SLA-backed.

## Verify
- [ ] `az acr show --query "{sku:sku.name,admin:adminUserEnabled,pna:publicNetworkAccess}"` → Premium/false/Disabled.
- [ ] `az acr check-health -n myacr --yes` and `az aks check-acr` pass from the cluster.
- [ ] A pipeline run builds via ACR Tasks, Defender shows the scan, and `notation verify` passes on the pushed digest.
- [ ] Purge task log shows deletions; `az acr show-usage` shows storage against the SKU limit.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-management-docs `container-registry` articles (skus, tasks-overview, artifact-cache-cli, auto-purge, retention-policy, soft-delete-policy, rbac-abac-repository-permissions, tutorial-sign-build-push, content-trust-deprecation, scan-images-defender, private-endpoints, image-lock, monitor; main branch) and the Azure CLI `acr` source.
- Confirmed: SKU feature split and default zone redundancy; `acr purge` flags run through `az acr run ... /dev/null`; retention policy needs `--status enabled`, Premium, preview; soft delete command, preview, 7-day default; `az acr cache create` options; task triggers and `--schedule`; `notation sign --plugin azure-kv`; DCT retirement 31 March 2028; Defender scan scope; log table names; 429 throttling; ABAC mode ignores AcrPull/AcrPush/AcrDelete.
- Removed as unconfirmed: quarantine mode, Resource Graph table name, Azure Policy name, per-service identity flag names, multi-arch via buildx, `.dockerignore` speed multiplier, Bicep publish, and the claim that each replica region needs its own private endpoint (the documentation says one private endpoint per VNet gets an extra IP per replica).
Method: documentation only; no commands were run.
