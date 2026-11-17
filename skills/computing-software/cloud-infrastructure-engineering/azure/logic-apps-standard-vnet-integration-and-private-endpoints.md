---
id: computing-software.cloud-infrastructure-engineering.azure.logic-apps-standard-vnet-integration-and-private-endpoints
name: logic-apps-standard-vnet-integration-and-private-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, logic-apps, logic-apps-vnet, logic-apps-private-endpoint, logic-apps-standard, storage-private-endpoints]
level: advanced
status: docs-checked
description: "Run Logic Apps Standard privately: outbound VNet integration, inbound private endpoints, private storage dependencies, and built-in connectors vs managed connectors."
sources: ["https://learn.microsoft.com/azure/logic-apps/secure-single-tenant-workflow-virtual-network-private-endpoint", "https://learn.microsoft.com/azure/logic-apps/deploy-single-tenant-logic-apps-private-storage-account", "https://learn.microsoft.com/azure/logic-apps/connectors/built-in"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logic Apps Standard networking

**Goal:** workflows that reach private resources and are not callable from the internet.

## Outbound: VNet integration
- Logic Apps Standard runs on the App Service (Workflow Standard) platform: enable **regional VNet integration** into a delegated subnet and route all outbound traffic through the VNet; see the secure-workflow page for the current subnet size and delegation requirements.
- **Built-in (in-app) connectors** (Service Bus, SQL, Blob, Event Hubs, HTTP) run in your app and go through the VNet. **Managed (shared) connectors** run in Microsoft's multi-tenant infrastructure and cannot reach private endpoints: prefer built-in connectors for private targets.

## Inbound: private endpoint
- Add a private endpoint on the logic app, set up private DNS, then restrict public access.
- Managed API webhook (push) triggers and actions do not work, because they run in the public cloud and cannot call into your private network.

## Private storage dependency
The app needs its storage account (`AzureWebJobsStorage`) for state. To lock storage down:
1. Private endpoints on the storage account for the services the app uses (see the private storage page for the list).
2. App settings: `WEBSITE_CONTENTOVERVNET=1` (content share over VNet), `WEBSITE_DNS_SERVER` if custom DNS.

## Gotchas
- Managed connectors run in Microsoft's multi-tenant infrastructure; target private resources with built-in connectors.

## Verify
- [ ] From outside, the workflow trigger URL is not reachable; from a VM in the VNet it runs.
- [ ] Workflow using built-in Service Bus connector reaches a namespace with public access disabled.

## Checked
2026-10-28. Confirmed on the Logic Apps secure single-tenant and private storage pages: `WEBSITE_CONTENTOVERVNET` set to 1, `WEBSITE_DNS_SERVER` for custom DNS, managed API webhook triggers/actions cannot reach private networks. Removed as unconfirmed: /26 subnet size, `vnetRouteAllEnabled`, sub-resource and DNS zone names, the storage sub-service list, file share precreation, managed-identity host storage setting, NAT and SCM advice, the 403 claim.
Method: documentation only; no commands were run.
