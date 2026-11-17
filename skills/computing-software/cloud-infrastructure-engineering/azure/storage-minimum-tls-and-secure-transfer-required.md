---
id: computing-software.cloud-infrastructure-engineering.azure.storage-minimum-tls-and-secure-transfer-required
name: storage-minimum-tls-and-secure-transfer-required
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, storage-security, minimum-tls, secure-transfer-required, tls-1-2, azure-policy]
level: practitioner
status: docs-checked
description: "Enforce TLS 1.2+ and HTTPS-only on storage accounts: find clients on old TLS from logs, set minimumTlsVersion and secure transfer, and govern with policy."
sources: ["https://learn.microsoft.com/azure/storage/common/transport-layer-security-configure-minimum-version", "https://learn.microsoft.com/azure/storage/common/storage-require-secure-transfer", "https://learn.microsoft.com/azure/storage/common/transport-layer-security-configure-client-version"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Minimum TLS and secure transfer required

**Goal:** no plaintext HTTP and no legacy TLS against your storage accounts.

## 1. Find old clients first
```kusto
StorageBlobLogs
| where TimeGenerated > ago(14d)
| summarize count() by TlsVersion, CallerIpAddress, UserAgentHeader
| where TlsVersion != "TLS 1.2" and TlsVersion != "TLS 1.3"
```
Repeat for the queue, table and file log tables. The `TlsVersion` property records the TLS version used for each logged request.

## 2. Enforce
```bash
az storage account update -g rg -n st --min-tls-version TLS1_2 --https-only true
az storage account show -g rg -n st --query "{tls:minimumTlsVersion, https:enableHttpsTrafficOnly}"
```
- Requests below the minimum fail with error code 400 (Bad Request) and a message that the TLS version isn't permitted.
- Azure Storage supports TLS 1.2 and 1.3; enforcing TLS 1.3 as the minimum isn't supported, and TLS 1.2 is the recommended minimum. Clients that support TLS 1.3 negotiate it automatically.
- Secure transfer required (HTTPS only) is enabled by default when you create a storage account; with it on, any request over HTTP is rejected.

## 3. Govern
Azure Policy has built-in definitions to require secure transfer and a minimum TLS version (a Deny effect blocks creating accounts that don't comply); see the built-in policy definitions list for the exact names.
```kusto
resources
| where type == "microsoft.storage/storageaccounts"
| where properties.minimumTlsVersion != "TLS1_2" or properties.supportsHttpsTrafficOnly == false
| project id, tls = properties.minimumTlsVersion, https = properties.supportsHttpsTrafficOnly
```

## Client fixes
See the Microsoft article on configuring a client application's TLS version for the supported settings per platform.

## Verify
- [ ] Logs show only TLS 1.2/1.3 for two weeks; ARG query returns no non-compliant accounts.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/common/transport-layer-security-configure-minimum-version, storage-require-secure-transfer): TLS 1.2 and 1.3 support, TLS 1.3 cannot be enforced as a minimum, TLS 1.2 recommended, HTTP 400 error for older clients, `TlsVersion` log property, secure transfer enabled by default and HTTP requests rejected, Azure Policy availability. Removed the unconfirmed NFS 3.0 secure-transfer statement, built-in policy display names, TLS 1.0/1.1 retirement remark and the .NET and Java client settings. `--min-tls-version` and `--https-only` are the az storage account update parameters used in the Microsoft examples for these settings.

Method: documentation only; no commands were run.
