---
id: computing-software.cloud-infrastructure-engineering.azure.apim-backup-restore-and-multi-region
name: apim-backup-restore-and-multi-region
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, api-management, apim-backup, apim-multi-region, disaster-recovery, availability-zones]
level: advanced
status: docs-checked
description: "Protect API Management with backup/restore to storage using managed identity, multi-region Premium deployments and zone redundancy."
sources: ["https://learn.microsoft.com/azure/api-management/api-management-howto-disaster-recovery-backup-restore", "https://learn.microsoft.com/azure/api-management/api-management-howto-deploy-multi-region", "https://learn.microsoft.com/azure/reliability/reliability-api-management"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# APIM backup, restore and multi-region

**Goal:** recover APIM configuration and keep the gateway serving during a regional outage.

## Options
| Need | Mechanism | Tier |
|---|---|---|
| Survive zone failure | Availability zones | Premium |
| Survive region failure, regional gateways | Multi-region deployment (additional locations) | Premium |
| Recover config after deletion or corruption | Backup/restore | Developer, Basic, Standard, Premium |

## Backup and restore
```powershell
$ctx = New-AzStorageContext -StorageAccountName stapimbk
Backup-AzApiManagement -ResourceGroupName rg -Name apim1 -StorageContext $ctx `
  -TargetContainerName backups -TargetBlobName "apim1.apimbackup" `
  -AccessType "SystemAssignedManagedIdentity"
Restore-AzApiManagement -ResourceGroupName rg -Name apim1-dr -StorageContext $ctx `
  -SourceContainerName backups -SourceBlobName "apim1.apimbackup" -AccessType "SystemAssignedManagedIdentity"
```
- Enable a managed identity on the APIM instance (on both instances when backing up and restoring to a different one) and assign it **Storage Blob Data Contributor** on the storage account.
- A restore is guaranteed only for 30 days after the backup was created; later restores fail with `Cannot restore: backup expired`.
- The target's pricing tier must match the backed-up service's tier. Don't change the service configuration (or scale or retier it) while a backup or restore runs; changes may be excluded or overwritten.
- Do not enable CORS on the storage account's Blob service. If the storage account has a firewall, use the managed identity and allow trusted Azure services.
- **Not backed up:** usage data used for analytics reports, custom domain TLS/SSL certificates, custom CA certificates, virtual network integration settings, managed identity configuration, Azure Monitor diagnostic configuration, protocols and ciphers settings, and developer portal content.
- Backup frequency sets your recovery point objective; take on-demand backups after changes. A Logic Apps sample for automating backups is linked from the Microsoft article.

## Multi-region
- Premium tier only. In the portal, open **Locations**, select **+ Add**, choose the region and the number of scale units, and **Save**; availability zones are configured automatically for the added region by default (recommended), or you can pick zones manually, in which case the units must distribute evenly across the zones.
- If the instance is in a virtual network, set up a virtual network and subnet in each added location first.
- By default each API still forwards to a single backend service URL; route to regional backends with policy when the backend is also multi-region.
- Read the Azure reliability guidance for API Management for the requirements and considerations for multi-region deployment.

## Verify
- [ ] Restore drill into a test instance succeeds within the 30-day backup window; record the duration.
- [ ] Every added location shows in **Locations** and responds.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (api-management-howto-disaster-recovery-backup-restore, api-management-howto-deploy-multi-region): backup tiers (Developer, Basic, Standard, Premium), managed-identity access type and Storage Blob Data Contributor role, 30-day restore guarantee and error text, tier-match and no-changes-during-backup constraints, no CORS on the Blob service, list of items not backed up (this corrects the earlier claim that custom domain certificates are included), multi-region Premium-only steps, zone configuration, backend routing caution. Removed the unconfirmed az apim CLI command, regional URL format, management-plane and developer-portal location claims, self-hosted gateway caching, the 30-minute restore duration and the GRS and Front Door remarks. The APIOps and Consumption-tier statements were dropped as unconfirmed.

Method: documentation only; no commands were run.
