---
id: computing-software.cloud-infrastructure-engineering.azure.acr-geo-replication-and-zone-redundancy
name: acr-geo-replication-and-zone-redundancy
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, container-registry, acr-geo-replication, acr-zone-redundancy, geo-replication, premium-registry, regional-endpoints]
level: practitioner
status: docs-checked
description: "Configure Premium ACR geo-replication and zone redundancy: add replicas, routing via Traffic Manager, regional endpoints, private endpoints per region and replication-lag gotchas."
sources: ["https://learn.microsoft.com/azure/container-registry/container-registry-geo-replication", "https://learn.microsoft.com/azure/container-registry/zone-redundancy", "https://learn.microsoft.com/azure/container-registry/container-registry-private-endpoints", "https://learn.microsoft.com/azure/container-registry/container-registry-soft-delete-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACR geo-replication and zone redundancy

**Goal:** clusters in every region pull images locally (fast, no cross-region egress) and the
registry survives a zone or region outage.

## Requirements
Geo-replication needs the Premium SKU. Zone redundancy is on by default for registries of every SKU and for
every geo-replica in regions that support availability zones, at no extra cost, and cannot be disabled there;
setting `zoneRedundancy: Enabled` in templates is harmless. For registries created before the default, read the
FAQ in the zone redundancy article.

## Add replicas
```bash
az acr replication create -r acrcontoso -l northeurope
az acr replication create -r acrcontoso -l eastus2
az acr replication list -r acrcontoso -o table
```
One login server name (`acrcontoso.azurecr.io`) for all regions; DNS-based global endpoint routing sends
requests to a healthy replica and fails over automatically (health-aware failover, minutes, not triggered by HTTP 429
throttling). All replicas are active and writable, and replication is eventually consistent.

## Routing control and regional endpoints
- Exclude a replica from global endpoint routing during an issue (it still receives replication and still accrues storage cost): `az acr replication update -r acrcontoso --name eastus2 --global-endpoint-routing false`. `--name` is the replication resource name from `az acr replication list`. In Azure CLI 2.86.0 and later `--region-endpoint-enabled` was renamed `--global-endpoint-routing`; the old name is removed in 2.87.0.
- Regional endpoints (preview, Premium, Azure CLI 2.86.0 or later) are per-replica login servers of the form `acrcontoso.<region>.geo.azurecr.io`; they bypass automatic failover, so clients must fail over themselves, and throttling limits are per replica.
- Dedicated data endpoints (`acrcontoso.northeurope.data.azurecr.io`) are per region; enable them for tight firewall allow-lists (the alternative is allowing `*.blob.core.windows.net`).

## Private endpoints
Create a private endpoint per region VNet; the private DNS zone is named `privatelink.azurecr.io`. A private endpoint
enables dedicated data endpoints automatically and consumes one private IP per geo-replica for its data endpoint, so
the zone needs records for the login server and for each regional data endpoint. Adding a replica later adds an IP
in each VNet that has a private endpoint.

## Replication behaviour to design around
- Push to region A, deploy immediately in region B: the pull can fail with `manifest unknown` until replication catches up. Re-pushing the same tag with different content can leave replicas resolving the tag to different digests for a while. Use webhooks (one per replica region) to learn when replication of a push completed, or deploy by digest after confirming it exists, or pin push and pull to one replica with a regional endpoint.
- Creating a replica takes time proportional to the registry size; existing replicas keep serving.
- Storage is billed per replica (1 GiB replicated to 5 replicas bills as 5 GiB); cross-region data transfer still applies to replication traffic.
- A multi-layer push that spans DNS changes can scatter layers and manifest across replicas and fail with manifest errors; pin the push (regional endpoint or a short-lived DNS cache).

## Gotchas
- Home region outage: image push, pull and delete continue through the remaining replicas, but registry configuration changes (network rules, replication settings) are unavailable until the home region recovers. The home region is fixed at creation.
- ACR Tasks are bound to the home region and do not run while it is down.
- Geo-replication doesn't protect against deletion — use soft delete (currently preview) and retention locks (`az acr repository update --write-enabled false --delete-enabled false`) for release images.

## Verify
- [ ] `az acr replication list -r acrcontoso -o table` shows every replica with a healthy (online) status.
- [ ] From a VM in each region: `nslookup acrcontoso.azurecr.io` resolves to the regional (or private) endpoint; pull time is local-fast.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-management-docs `container-registry` articles (geo-replication, zone-redundancy, private-endpoints, soft-delete-policy, image-lock; main branch) and the Azure CLI `acr` module source.
- Confirmed and corrected: zone redundancy is default and cannot be disabled; `--region-endpoint-enabled` replaced by `--global-endpoint-routing` (CLI 2.86.0, old name removed in 2.87.0) and addressed by replication name; routing is DNS-based health-aware failover, not Traffic Manager; regional endpoint form `<registry>.<region>.geo.azurecr.io` (preview); data endpoint form `<registry>.<region>.data.azurecr.io`; `privatelink.azurecr.io`; eventual consistency and `manifest unknown`; home region outage and Tasks behaviour; storage billed per replica; soft delete is preview; `--write-enabled false --delete-enabled false` lock.
- Removed as unconfirmed: polling `az acr manifest show`, the `--location` option on webhook creation, the "deleting a replica deletes its data" claim, and the agent-pool region remark.
Method: documentation only; no commands were run.
