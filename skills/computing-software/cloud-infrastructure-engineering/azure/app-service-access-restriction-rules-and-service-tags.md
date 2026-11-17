---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-access-restriction-rules-and-service-tags
name: app-service-access-restriction-rules-and-service-tags
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service-networking, access-restrictions, access-restriction-rules, ip-restrictions, scm-restrictions, service-tags, x-azure-fdid]
level: practitioner
status: docs-checked
description: "Lock App Service inbound with access restriction rules: IP ranges, service tags, VNet subnets, Front Door ID header filtering, SCM-site rules and default action."
sources: ["https://learn.microsoft.com/azure/app-service/app-service-ip-restrictions", "https://learn.microsoft.com/azure/app-service/overview-access-restrictions", "https://learn.microsoft.com/azure/frontdoor/origin-security"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Service access restriction rules and service tags

**Goal:** the app only accepts traffic from its front door (Front Door, App Gateway, APIM, known
IPs), while keeping the deployment (SCM) site reachable for pipelines.

## Rule types
| Type | Example | Notes |
|---|---|---|
| IPv4/IPv6 range | `203.0.113.0/24` | Limit of 512 rules; multi-source rules combine up to eight IP ranges or eight service tags |
| Service tag | `AzureFrontDoor.Backend` | Tag ranges are Microsoft-maintained |
| VNet subnet | App Gateway subnet | Uses service endpoint `Microsoft.Web` on that subnet |
| HTTP header filter | `X-Azure-FDID: <your-front-door-id>` combined with the service tag | Stops *other* Front Door tenants |

## Front Door only
```bash
fdid=<your-front-door-id>   # the profile's Front Door ID, shown on its Overview page
az webapp config access-restriction add -g rg -n app-orders --rule-name afd --action Allow \
  --priority 100 --service-tag AzureFrontDoor.Backend --http-headers x-azure-fdid=$fdid
az webapp config access-restriction set -g rg -n app-orders --default-action Deny
```
## App Gateway subnet
```bash
az webapp config access-restriction add -g rg -n app-orders --rule-name agw --action Allow --priority 110 \
  --vnet-name vnet-hub --subnet snet-agw --vnet-resource-group rg-net
```
(Adds the `Microsoft.Web` service endpoint to the subnet if allowed — needs network permissions.)

## SCM (Kudu) site
The SCM site can use the main site's rules or its own (`--use-same-restrictions-for-scm-site`). Typical:
```bash
az webapp config access-restriction set -g rg -n app-orders --use-same-restrictions-for-scm-site false
az webapp config access-restriction add -g rg -n app-orders --scm-site true --rule-name devops-agents \
  --action Allow --priority 100 --ip-address 198.51.100.10/32
az webapp config access-restriction set -g rg -n app-orders --scm-default-action Deny
```
Prefer self-hosted agents with fixed IPs or private endpoints for deployments.

## Evaluation
Rules evaluate by priority (lowest number first); first match wins; default action applies when
nothing matches. Blocked requests get a 403 response.

## Gotchas
- Service tag alone (`AzureFrontDoor.Backend`) allows every Front Door customer — always add the FDID header.
- Access restrictions govern the public endpoint; traffic arriving through a private endpoint is governed by the private endpoint (see the overview article).
- Functions: restrictions also block the portal's "Test/Run" and log streaming from your browser unless your IP is allowed.
- IP restrictions are a per-slot setting that does not swap unless configured to.

## Verify
- [ ] `az webapp config access-restriction show -g rg -n app-orders` lists rules and both default actions.
- [ ] Direct `curl https://app-orders.azurewebsites.net` → 403; through Front Door → 200.
- [ ] Pipeline deployment still succeeds against SCM.

## Checked
2026-10-27. Confirmed on Microsoft Learn: app-service-ip-restrictions (512-rule limit, multi-source rules of eight ranges or tags), CLI reference for
`az webapp config access-restriction` (--rule-name, --action, --priority, --service-tag, --http-headers, --vnet-name, --subnet, --vnet-resource-group,
--ip-address, --scm-site, --default-action, --scm-default-action, --use-same-restrictions-for-scm-site).
Corrected: `--http-header` to `--http-headers`. Removed: the `scmIpSecurityRestrictionsUseMain` default claim, the "403 Ip Forbidden" exact text, the
private-endpoint bypass wording, the slot-swap claim narrowed to the documented IP restrictions behaviour.

Method: documentation only; no commands were run.
