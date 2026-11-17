---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-private-endpoints-for-inbound
name: app-service-private-endpoints-for-inbound
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service-networking, app-service-private-endpoint, inbound-private-endpoint, privatelink-azurewebsites, scm-site, public-network-access]
level: practitioner
status: docs-checked
description: "Make an App Service or Function reachable only privately: private endpoint for site and slots, privatelink.azurewebsites.net DNS, SCM access, and App Gateway or Front Door."
sources: ["https://learn.microsoft.com/azure/app-service/overview-private-endpoint", "https://learn.microsoft.com/azure/app-service/networking/private-endpoint", "https://learn.microsoft.com/azure/private-link/private-endpoint-dns#web"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Service private endpoints for inbound

**Goal:** the app (and its Kudu/SCM site) has no public ingress; users and pipelines reach it
through private networking or a WAF front end with Private Link.

## Create
```bash
az network private-endpoint create -g rg-net -n pe-app-orders --vnet-name vnet-spoke --subnet snet-pe \
  --private-connection-resource-id $(az webapp show -g rg -n app-orders --query id -o tsv) \
  --group-id sites --connection-name app-orders
```
Then add a DNS zone group (`az network private-endpoint dns-zone-group create`) for `privatelink.azurewebsites.net`, and disable public network access on the app (portal: Networking, public network access Disabled).
When you enable a private endpoint, disable public network access to remove public exposure.
Slots: separate private endpoint with `--group-id sites-<slotname>`.
Supported on Basic, Standard, Premium v2/v3/v4, Isolated v2 and Functions Premium plans.

## DNS
The `sites` sub-resource maps to the zones `privatelink.azurewebsites.net` and `scm.privatelink.azurewebsites.net` (the app and its SCM site).
Public DNS CNAMEs `app-orders.azurewebsites.net → app-orders.privatelink.azurewebsites.net`; clients
must resolve that via the private zone (linked to the VNets / via Private Resolver for on-prem).
Custom domains: keep the custom hostname CNAME to `app-orders.azurewebsites.net` and ensure the
private chain resolves.

## Deployments with public access disabled
- Pipelines must reach the **SCM** endpoint privately: self-hosted agents/runners in a peered VNet, or managed DevOps pools with VNet injection.
- Alternatively keep public access enabled with access restrictions that deny the main site and allow the SCM site only from agent IPs (separate SCM rules).

## Front ends
- **App Gateway** in the VNet → backend = app hostname resolving privately; set host override to the app's hostname.
- **Front Door Premium** → Private Link origin to the app (`sites` group ID); approve the private endpoint connection on the app.

## Gotchas
- Private endpoint is **inbound only**; outbound still needs VNet integration.
- Enabling a private endpoint does not by itself remove public access — disable public network access explicitly and verify.
- Availability tests from the internet will fail once public access is off — run them from inside the network.

## Verify
- [ ] From the internet: `curl -I https://app-orders.azurewebsites.net` → blocked (403 or connection refused).
- [ ] From the VNet: `nslookup app-orders.azurewebsites.net` returns the PE IP and the site responds.
- [ ] Pipeline deploy to SCM succeeds from the private agent.

## Checked
2026-10-27. Confirmed on Microsoft Learn: overview-private-endpoint (supported plans Basic through Isolated v2 and Functions Premium, slot sub-resource `sites-<slot-name>`,
one endpoint per slot, disable public network access for isolation), private-endpoint-dns (sites zone `privatelink.azurewebsites.net` and `scm.privatelink.azurewebsites.net`),
CLI reference for `az network private-endpoint` (--group-id, --connection-name, --private-connection-resource-id, dns-zone-group create exists).
Removed: dns-zone-group flags and the `az webapp update --set publicNetworkAccess` command (not confirmed on a fetched reference), the "two records in one zone" wording,
`scmIpSecurityRestrictionsUseMain`, run-from-package and Functions storage statements, exact 403 text.

Method: documentation only; no commands were run.
