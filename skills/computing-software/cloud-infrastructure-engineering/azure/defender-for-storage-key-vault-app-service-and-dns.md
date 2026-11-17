---
id: computing-software.cloud-infrastructure-engineering.azure.defender-for-storage-key-vault-app-service-and-dns
name: defender-for-storage-key-vault-app-service-and-dns
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, defender-for-cloud, defender-for-key-vault, defender-for-app-service, defender-for-dns, defender-for-storage]
level: practitioner
status: docs-checked
description: "What Defender for Storage, Key Vault, App Service and DNS detect, and how to respond to their common alerts."
sources: ["https://learn.microsoft.com/azure/defender-for-cloud/defender-for-key-vault-introduction", "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-app-service-introduction", "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-dns-introduction", "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-storage-introduction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defender for Storage, Key Vault, App Service and DNS

**Goal:** threat detection on the PaaS data planes most often abused, with known
responses for their common alerts.

## Plans at a glance
| Plan | Detects |
|---|---|
| **Storage** | Malicious file uploads (on-upload and on-demand malware scanning), sensitive data exfiltration, data corruption, sensitive data threat detection |
| **Key Vault** | Unusual and potentially harmful attempts to access or exploit Key Vault accounts, including suspicious activity from stolen credentials |
| **App Service** | Threats against App Service resources, and dangling DNS entries left after a site is decommissioned |
| **DNS** | Data exfiltration by DNS tunnelling, and communication with domains used for phishing or crypto mining |

## Storage specifics
- Malware scanning is charged per GB scanned, with a monthly cap on uploaded scanned data that can be set subscription-wide or per storage account. The default is 10,000 GB of uploaded blobs per month per storage account; scanning stops for remaining blobs once the cap is exceeded. Two alerts warn as usage approaches the cap (the first at 75%).
- Scanning also adds charges for storage read operations, blob indexing and Event Grid notifications.
- Automated response: integrate with Azure Event Grid, then connect Azure Functions or Logic Apps to delete, quarantine or alert on malicious blobs.

## Key Vault response
Do not dismiss an alert because you recognise the user or application; the plan targets stolen-credential activity. Contact the owner to confirm the activity was legitimate, then rotate the secrets, keys and certificates the suspicious identity accessed. A suppression rule can be created for confirmed-benign activity.

## App Service
A dangling DNS alert fires when an App Service site is decommissioned but its custom domain DNS entry is not deleted. The entry then points to a nonexistent resource and the subdomain can be taken over. Defender does not scan the registrar for pre-existing dangling entries. Remove the DNS record. To investigate App Service alerts, enable diagnostic settings on the App Service resource (this can add storage cost).

## DNS
For new subscriptions, suspicious-DNS alerts are included in Defender for Servers Plan 2 (P2).

## Gotchas
- Defender for Storage (classic) must be migrated to the new pricing plan to get current features and pricing.
- App Service protection works on any App Service tier; billing is by total compute instances across all plan tiers.

## Verify
- [ ] The plans show as enabled on production subscriptions in Defender for Cloud environment settings.

## Checked
Method: docs-checked 2026-11-09 against the Learn pages for Defender for Key Vault, App Service, DNS and Storage introductions (downloaded with curl; detection, cost-cap, dangling DNS, response and billing sections read). Dropped unconfirmed CLI commands, the Resource Manager plan, KQL, blob index tag name and web-shell claims.
