---
id: computing-software.cloud-infrastructure-engineering.azure.acr-login-and-pull-troubleshooting-with-check-health
name: acr-login-and-pull-troubleshooting-with-check-health
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, container-registry, acr-check-health, acr-troubleshooting, imagepullbackoff, check-acr, acrpull]
level: practitioner
status: docs-checked
description: "Fix ACR login and pull failures: az acr check-health, token expiry, RBAC vs repository tokens, private endpoint DNS and data endpoints, and AKS ImagePullBackOff."
sources: ["https://learn.microsoft.com/azure/container-registry/container-registry-check-health", "https://learn.microsoft.com/azure/container-registry/container-registry-troubleshoot-login-authn-authz", "https://learn.microsoft.com/azure/container-registry/container-registry-authentication", "https://learn.microsoft.com/azure/container-registry/container-registry-firewall-rules", "https://learn.microsoft.com/azure/aks/cluster-container-registry-integration", "https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/connectivity/cannot-pull-image-from-acr-to-aks-cluster"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACR login and pull troubleshooting

**Goal:** turn `unauthorized`, `denied` and `ImagePullBackOff` into a specific fix.

## Start here
```bash
az acr check-health -n crcorp --yes          # environment checks plus access to the named registry
az acr check-health -n crcorp --vnet vnet-app --yes   # verify DNS routes to the private endpoint (pass the VNet resource ID if it is in another group or subscription)
az acr check-health -n crcorp --ignore-errors --yes   # report every check instead of stopping at the first error
```

## Error map
| Error | Cause | Fix |
|---|---|---|
| `unauthorized: authentication required` | No/expired token (az acr login tokens are valid for 3 hours) | Re-login; in CI login per job |
| `denied: requested access to the resource is denied` | Identity lacks AcrPull/AcrPush, or repository-scoped token lacks the repo | Grant the role at registry scope; check the token scope map; ContainerRegistryLoginEvents logs (if enabled) show the identity and IP |
| `403 Forbidden` on login or pull from a network | Registry firewall or public network access disabled | Add an IP rule, or use the private endpoint path (see the network troubleshooting article) |
| DNS resolves to public IP while public access disabled | Private DNS zone missing/unlinked | `privatelink.azurecr.io` zone with both `<reg>` and `<reg>.<region>.data` records linked to the VNet |
| Pull starts then fails on layers | Data endpoint blocked (`<reg>.<region>.data.azurecr.io`, or `*.blob.core.windows.net` when dedicated data endpoints are off) | Allow the data endpoint FQDNs in the firewall |
| `manifest unknown` | Tag doesn't exist / was purged, or (geo-replicated) replication has not finished | Check `az acr repository show-tags`; wait for replication |

## Non-docker environments
```bash
TOKEN=$(az acr login -n crcorp --expose-token --query accessToken -o tsv)
podman login crcorp.azurecr.io -u 00000000-0000-0000-0000-000000000000 -p "$TOKEN"
```

## AKS ImagePullBackOff
```bash
kubectl describe pod <pod>
az aks check-acr -g rg -n aks01 --acr crcorp.azurecr.io      # validates that the cluster can reach the registry
az aks update -g rg -n aks01 --attach-acr crcorp             # assigns AcrPull to the agent pool (kubelet) managed identity
```
The identity associated with the agent pool (the **kubelet identity**) needs AcrPull. `--attach-acr` is not supported for ABAC-enabled registries (role assignment mode "RBAC Registry + ABAC Repository Permissions"); use the Container Registry Repository Reader role there. With egress through a firewall, allow the registry and data endpoints.

## Gotchas
- Admin user credentials work with `docker login` and hide RBAC problems - keep admin disabled.
- Geo-replicated registries resolve to the nearest replica; a replica's data endpoint must be allowed too.

## Verify
- [ ] check-health clean from the client network; test pod pulls the image; firewall logs show no denies for registry FQDNs.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-management-docs (container-registry check-health, authentication, firewall-rules, troubleshoot-login-authn-authz), MicrosoftDocs/azure-aks-docs (cluster-container-registry-integration) and the Azure CLI `acr` and `acs` source (`--vnet`, `--ignore-errors`, `--yes`, `aks check-acr --acr`, `--attach-acr`).
- Confirmed: 3-hour `az acr login` token, `--expose-token` with the all-zero GUID username, `check-health` flags, `*.blob.core.windows.net` versus dedicated data endpoints, AcrPull on the agent pool identity, ABAC limitation of `--attach-acr`.
- Removed as unconfirmed: the exact `client with IP ... is not allowed access` message (replaced by the documented 403 case), the anonymous pull gotcha, and descriptive claims about what `check-acr` validates internally.
Method: documentation only; no commands were run.
