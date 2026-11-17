---
id: computing-software.cloud-infrastructure-engineering.azure.azure-functions-vnet-integration-and-private-endpoints
name: azure-functions-vnet-integration-and-private-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-functions, functions-vnet, functions-private-endpoint, private-storage-account, flex-consumption, vnet-integration]
level: advanced
status: docs-checked
description: "Run Azure Functions fully private: VNet integration for outbound, private endpoints for inbound, a locked-down host storage account, and Flex/Premium plan specifics."
sources: ["https://learn.microsoft.com/en-us/azure/azure-functions/functions-networking-options", "https://learn.microsoft.com/en-us/azure/azure-functions/configure-networking-how-to", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-vnet", "https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-plan", "https://learn.microsoft.com/en-us/azure/azure-functions/manage-connections"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Functions VNet integration and private endpoints

**Goal:** a Function app whose triggers, host storage and dependencies are all private, without
breaking scale or deployments.

## Plan support
| Plan | VNet integration (outbound) | Private endpoint (inbound) | Private host storage |
|---|---|---|---|
| Flex Consumption | Yes (subnet delegated to `Microsoft.App/environments`) | Yes | Yes |
| Premium (EP) | Yes | Yes | Yes (with content share settings) |
| Dedicated | Yes | Yes | Yes |
| Consumption (classic) | No | No | No |

## Steps (Premium/Flex)
1. **Subnets**: integration subnet (Flex: delegate to `Microsoft.App/environments`; Premium: `Microsoft.Web/serverFarms`), PE subnet.
2. **Host storage account** private: private endpoints for the `file`, `blob` and `table` subresources (and `queue` for Durable Functions) with DNS; `publicNetworkAccess=Disabled`.
3. **Identity-based host storage** (recommended): `AzureWebJobsStorage__accountName=<acct>`, `__credential=managedidentity`; roles *Storage Blob Data Owner* (the documented minimum), *Storage Table Data Contributor* (diagnostic events, Durable Functions) and *Storage Queue Data Contributor* (blob trigger, Durable Functions, some extensions); Account Contributor only where a binding's docs list it.
4. Premium: set the `vnetContentShareEnabled` site property (replaces the legacy `WEBSITE_CONTENTOVERVNET` setting) so the Azure Files content share is reached via the VNet; create the file share as part of the deployment and set `WEBSITE_CONTENTSHARE`.
5. Enable VNet integration + Route All (needed to block traffic to public addresses); ensure VNet DNS resolves privatelink zones.
6. Inbound private endpoint on the function app and public network access disabled if callers are private (not available on Consumption).
7. Triggers from private resources (Service Bus, Event Hubs with PE): Premium needs **runtime scale monitoring** (`functionsRuntimeScaleMonitoringEnabled`) so non-HTTP triggers secured by a virtual network can scale; Flex needs no extra configuration.

```bash
az resource update -g rg -n func-orders/config/web --set properties.functionsRuntimeScaleMonitoringEnabled=1 --resource-type Microsoft.Web/sites
```

## Deployment with private everything
- With a private deployment endpoint, the machine, runner or agent that deploys must have network connectivity and DNS resolution for it (for example a self-hosted agent in the VNet).
- Flex Consumption deploys the package to its deployment storage container, so the deploying identity needs access to that account.

## Gotchas
- For automated creation of a secured Premium app, set `vnetContentShareEnabled`, create the file share in the deployment and set `WEBSITE_CONTENTSHARE` (see the docs' secured deployment templates).
- A host that cannot start usually cannot reach its storage: check DNS, private endpoints, firewall and roles.

## Verify
- [ ] Portal shows functions listed (host reachable) and runtime version.
- [ ] Storage account has no public access and the app still runs; the storage endpoints resolve to private IPs from the integration subnet.
- [ ] Service Bus-triggered function scales out under backlog (instance count metric).

## Checked
Checked 2026-10-24 against azure-docs azure-functions pages (functions-networking-options, configure-networking-how-to, flex-consumption-plan, functions-app-settings, manage-connections, functions-scale). Confirmed: integration subnet delegation Microsoft.App/environments (Flex) and Microsoft.Web/serverFarms (Premium, Dedicated); Consumption has no VNet integration or private endpoints; Flex needs no extra runtime scale monitoring configuration; functionsRuntimeScaleMonitoringEnabled for Premium with the az resource update command; vnetContentShareEnabled replaces WEBSITE_CONTENTOVERVNET; private endpoints for file, blob, table (queue for Durable); Route All requirement for blocking public traffic. Removed unconfirmed: the sites sub-resource name, the runtime-unreachable error text, timer and queue role statements, the nameresolver check.

Method: documentation only; no commands were run.
