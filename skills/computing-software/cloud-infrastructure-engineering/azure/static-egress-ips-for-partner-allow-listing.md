---
id: computing-software.cloud-infrastructure-engineering.azure.static-egress-ips-for-partner-allow-listing
name: static-egress-ips-for-partner-allow-listing
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, outbound-connectivity, egress-allowlist, static-egress, nat-gateway, public-ip-prefix, app-service]
level: practitioner
status: docs-checked
description: "Give partners a small, stable set of source IPs from Azure: NAT gateway with prefixes, firewall SNAT, and per-service options for App Service, Functions, AKS and Container Apps."
sources: ["https://learn.microsoft.com/azure/app-service/networking/nat-gateway-integration", "https://learn.microsoft.com/azure/nat-gateway/nat-overview", "https://learn.microsoft.com/azure/firewall/snat-private-range"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static egress IPs for partner allow-listing

**Goal:** "Please allow these 2 IPs" - and they don't change when you scale, redeploy or move plans.

## The standard answer: NAT gateway + public IP prefix
1. Public IP prefix (a range you can hand to the partner as a single entry).
2. NAT gateway using IPs from the prefix, attached to the subnets that call partners.
3. Give partners the **whole prefix**, not individual IPs.
```bash
az network public-ip prefix show -g rg-net -n ippre-egress --query ipPrefix -o tsv
```

## Per service
| Service | How to get static egress |
|---|---|
| App Service | Regional VNet integration plus a NAT gateway on the integration subnet (see the App Service NAT gateway integration page) |
| Through hub firewall | Azure Firewall public IPs; see the Azure Firewall SNAT private range page for SNAT behaviour |

For other services, take the outbound design from that service's own networking docs.

## Operational rules
- Document egress IPs per environment; tag the public IP resources (`purpose=partner-egress`).
- Protect the IPs/prefix with a CanNotDelete lock - a recreated IP is a different address.
- Before changing egress design, send partners the new IPs and run both paths in parallel where possible.

## Gotchas
- NAT gateway doesn't work with Basic SKU resources such as a Basic load balancer or Basic public IP; upgrade them to Standard.
- Confirm what the partner actually enforces (IP list, client certificates).

## Verify
- [ ] `curl https://ifconfig.me` (or a partner echo endpoint) from each workload returns an IP inside the documented prefix.

## Checked
2026-10-28. Confirmed on the NAT gateway overview and App Service NAT gateway integration pages: NAT gateway with a public IP address or public IP prefix, App Service regional VNet integration plus NAT gateway for a static outbound address, Basic SKU resources do not work with NAT gateway; the Azure Firewall SNAT private range page was fetched for the firewall row.
Removed (not confirmed): prefix sizes, connection spreading claim, VM/AKS/Container Apps/Functions rows and `possibleOutboundIpAddresses`, and the private endpoint traffic note.

Method: documentation only; no commands were run.
