---
id: computing-software.cloud-infrastructure-engineering.azure.enable-managed-identity-on-app-service-functions-vms-and-aks
name: enable-managed-identity-on-app-service-functions-vms-and-aks
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-identity, enable-managed-identity, mi-on-app-service, mi-on-vm, kubelet-identity, aks-identity]
level: practitioner
status: docs-checked
description: "Enable system or user-assigned managed identities on App Service, Functions, VMs/VMSS, Container Apps and AKS (control plane, kubelet), with CLI and Bicep."
sources: ["https://learn.microsoft.com/azure/app-service/overview-managed-identity", "https://learn.microsoft.com/azure/container-apps/managed-identity", "https://learn.microsoft.com/azure/aks/use-managed-identity", "https://learn.microsoft.com/azure/aks/pre-created-kubelet-managed-identity", "https://learn.microsoft.com/azure/aks/system-assigned-managed-identity"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable managed identity on App Service, Functions, VMs and AKS

**Goal:** each compute service runs with the intended identity and the app knows which one to use.

## App Service / Functions
```bash
az webapp identity assign -g rg -n app-orders                              # system-assigned
az webapp identity assign -g rg -n app-orders --identities <uami-resource-id>
```
- Managed identity configuration is specific to the **slot**: configure each slot's identity separately (go to the slot first in the portal).
- Adding an identity restarts the app. To create or assign identities you need write permission on the app (for example Website Contributor) and, for user-assigned identities, the assign action on the identity.
- Managed identities are not available for apps deployed in Azure Arc, and they do not support cross-directory scenarios.

## VM / VMSS
Use `az vm identity assign` and `az vmss identity assign` with `--identities`; see the managed identity quickstarts for VMs and scale sets for the exact options.

## Container Apps
```bash
az containerapp identity assign -n ca-orders -g rg --user-assigned <uami-id>
az containerapp identity assign -n ca-orders -g rg --system-assigned
```

## AKS — three different identities
| Identity | Used for | Configure |
|---|---|---|
| Cluster (control plane) | Authorize AKS to other Azure resources | `--assign-identity <uami-id>` at create |
| Kubelet | Pull from ACR | `--assign-kubelet-identity <uami-id>` (pre-created kubelet identity); `az aks update --attach-acr` grants AcrPull |
| Workload identity | Pods | Federated credentials on a UAMI (separate skill) |
Moving an existing cluster to a user-assigned identity uses `az aks update --enable-managed-identity --assign-identity <id>`; it only works when a newer node image (VHD) is available to consume, and you must re-run `az aks update --attach-acr` afterwards if the cluster pulls from ACR. Updating the kubelet identity (`--assign-kubelet-identity`) upgrades the node pools, so configure PodDisruptionBudgets first. A cluster created with a managed identity cannot be switched back to a service principal.

## Bicep snippet
```bicep
identity: { type: 'SystemAssigned, UserAssigned', userAssignedIdentities: { '${uami.id}': {} } }
```
Check the resource provider's identity schema for the exact `type` values.

## Gotchas
- A system-assigned identity is tied to the resource: recreating the resource creates a new principal.
- Do not assume the token request URL for an app: read it from the `IDENTITY_ENDPOINT` environment variable the platform sets.

## Verify
- [ ] `az webapp identity show -g rg -n app-orders` / `az vm identity show` lists the expected identities.
- [ ] `az aks show -g rg -n aks --query identity` shows the control plane identity you expect.
- [ ] The app can obtain a token for the expected identity.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-docs (app-service/overview-managed-identity, container-apps/managed-identity) and MicrosoftDocs/azure-aks-docs (user-assigned-managed-identity, system-assigned-managed-identity, pre-created-kubelet-managed-identity; main branch).
- Confirmed: `az webapp identity assign --identities`; slot-specific identity; app restarts on change; Arc and cross-directory limits; `az containerapp identity assign --system-assigned/--user-assigned`; AKS `--assign-identity`, `--assign-kubelet-identity`, update caveats (VHD update needed, re-run `--attach-acr`, kubelet identity update upgrades node pools); no switching back to a service principal.
- Removed as unconfirmed: slot swap behaviour, `keyVaultReferenceIdentity`, Functions identity-based connection settings, VM and VMSS command details, `az containerapp registry set`, Network Contributor requirement, and the node-image-only upgrade step.
Method: documentation only; no commands were run.
