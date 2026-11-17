---
id: computing-software.cloud-infrastructure-engineering.azure.functions-azurewebjobsstorage-and-identity-based-host-storage
name: functions-azurewebjobsstorage-and-identity-based-host-storage
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-functions, azurewebjobsstorage, host-storage, identity-based-connections, content-share]
level: practitioner
status: docs-checked
description: "Run Functions host storage without keys: AzureWebJobsStorage__accountName with managed identity, required roles, content share caveats and locked-down storage."
sources: ["https://learn.microsoft.com/en-us/azure/azure-functions/manage-connections", "https://learn.microsoft.com/en-us/azure/azure-functions/storage-considerations", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-app-settings", "https://learn.microsoft.com/en-us/azure/azure-functions/configure-networking-how-to"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AzureWebJobsStorage and identity-based host storage

**Goal:** the Functions host's own storage (keys, timers, leases, Durable state) uses managed identity, not an
account key in an app setting.

## What host storage is for
Function keys/secrets (blob), timer trigger schedule monitors and singleton leases, blob trigger receipts,
Event Hubs checkpoints, Durable Functions task hub (queues/tables/blobs). Not your application data.

## Identity-based configuration
Replace `AzureWebJobsStorage=<connection string>` with:
```
AzureWebJobsStorage__accountName = stfuncorders
# user-assigned identity:
AzureWebJobsStorage__credential = managedidentity
AzureWebJobsStorage__clientId   = <uami-client-id>
```
Roles on the storage account for the app identity:
- **Storage Blob Data Owner**: the documented minimum for the host-required `AzureWebJobsStorage` connection,
- **Storage Table Data Contributor**: lets the host persist diagnostic events (without it you can see warnings in the logs) and is needed by Durable Functions,
- **Storage Queue Data Contributor**: for the blob trigger (alongside Blob Data Owner), Durable Functions and some extensions,
- Storage Account Contributor only where a binding's documentation lists it.

## Content share (Windows Consumption and Elastic Premium)
Apps on a Windows Consumption plan or an Elastic Premium plan (Windows or Linux) get an Azure Files share by default, configured with `WEBSITE_CONTENTAZUREFILECONNECTIONSTRING` + `WEBSITE_CONTENTSHARE`. Azure Files **does not support identity-based connections**, so a connection string is required. Options: keep the key in that setting (as a Key Vault reference with `WEBSITE_SKIP_CONTENTSHARE_VALIDATION=1` and a pre-created share), create the app without the Azure Files dependency (scaling might be limited), or use **Flex Consumption**, which supports managed identity connections for its deployment package.

## Network-restricted storage
- Function app needs VNet integration; the storage account gets private endpoints for the `file`, `blob` and `table` subresources (and `queue` for Durable Functions), with DNS.
- When the content share is behind a virtual network, set the `vnetContentShareEnabled` site property (the legacy `WEBSITE_CONTENTOVERVNET` setting is replaced by it); apps in the same plan, including slots, should use the same value.

## Gotchas
- Remove the old `AzureWebJobsStorage` connection string setting so only the identity-based settings remain.
- Sharing one host storage account across function apps can cause host ID collisions (the host ID is computed from the app name, truncated, so long similar names collide): use separate accounts, shorten the name, or set `AzureFunctionsWebHost__hostid`. Changing the host ID or storage account can make blob triggers reprocess blobs.
- Do not apply lifecycle management policies to the host storage account; Functions keeps important state in blobs.

## Verify
- [ ] App starts and timer/blob triggers fire with no account key in configuration; storage logs show OAuth authentication.

## Checked
Checked 2026-10-24 against azure-docs azure-functions pages (manage-connections, storage-considerations, functions-app-settings, configure-networking-how-to, flex-consumption-plan). Confirmed: AzureWebJobsStorage__accountName, __credential=managedidentity, __clientId; Storage Blob Data Owner as the documented minimum plus Table Data Contributor for diagnostic events; Azure Files has no identity-based connection support; content share default on Windows Consumption and Elastic Premium; private endpoints for file, blob, table (and queue for Durable); vnetContentShareEnabled replaces WEBSITE_CONTENTOVERVNET; host ID collision strategies and AzureFunctionsWebHost__hostid. Found wrong and fixed: content share was said to apply to Linux Consumption; Table Data Contributor was described as Durable-only. Removed unconfirmed: connection-string precedence, Dedicated plan content-share statement, portal warning note.

Method: documentation only; no commands were run.
