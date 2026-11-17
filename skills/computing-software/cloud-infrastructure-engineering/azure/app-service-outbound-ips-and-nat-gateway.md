---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-outbound-ips-and-nat-gateway
name: app-service-outbound-ips-and-nat-gateway
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service-networking, outbound-ips, app-service-nat-gateway, static-egress-ip, snat, possibleoutboundipaddresses]
level: practitioner
status: docs-checked
description: "Get predictable App Service egress IPs: outboundIpAddresses vs possibleOutboundIpAddresses, when they change, and a static IP via VNet integration + NAT gateway."
sources: ["https://learn.microsoft.com/azure/app-service/overview-inbound-outbound-ips", "https://learn.microsoft.com/azure/app-service/networking/nat-gateway-integration", "https://learn.microsoft.com/azure/app-service/troubleshoot-intermittent-outbound-connection-errors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Service outbound IPs and NAT gateway

**Goal:** partners can allow-list your app's egress IP, and the app doesn't suffer SNAT
exhaustion under load.

## Default outbound IPs
```bash
az webapp show -g rg -n app-orders --query "{current:outboundIpAddresses, possible:possibleOutboundIpAddresses}" -o json
```
- `outboundIpAddresses`: what the app uses now (shared with other apps in the same scale unit).
- `possibleOutboundIpAddresses`: everything it could use after scaling to another tier/scale unit.
- The set of outbound IPs can change when you scale between tiers or the app moves between deployment units; allow-list every address in the *possible* list, and note that these IPs are shared with other customers.
- Premium v4 does not provide a stable set of outbound IPs (the portal shows "Dynamic" and the CLI properties return empty strings); use a NAT gateway for a stable egress IP.

## Static egress with NAT gateway
1. Regional VNet integration on the app (delegated subnet).
2. Route-all on (`vnetRouteAllEnabled=true`) so internet-bound traffic enters the VNet.
3. NAT gateway with a Standard public IP or prefix attached to the **integration subnet**.
```bash
az network public-ip create -g rg-net -n pip-nat-app --sku Standard --zone 1
az network nat gateway create -g rg-net -n ng-app --public-ip-addresses pip-nat-app --zone 1
az network vnet subnet update -g rg-net --vnet-name vnet-spoke -n snet-app-int --nat-gateway ng-app
az webapp config set -g rg -n app-orders --vnet-route-all-enabled true
```
Now egress to the internet is the NAT public IP, dedicated to you; NAT gateway also gives SNAT
ports per IP (64,512 per IP address, up to 16 IP addresses) and mitigates SNAT port exhaustion.
Alternative: route-all + UDR 0.0.0.0/0 to Azure Firewall → egress via firewall public IP (inspection + logging).

## SNAT exhaustion symptoms without NAT
Intermittent connection errors or timeouts to external endpoints under load; the *Diagnose and solve problems* blade covers SNAT port exhaustion. Fix in code too: reuse connections (connection pooling, keep-alive).

## Gotchas
- Calls to Azure services over private endpoints stay private and don't use the NAT gateway.

## Verify
- [ ] From Kudu: `curl -s https://ifconfig.me` returns the NAT public IP.
- [ ] SNAT diagnostics show no port exhaustion at peak.

## Checked
2026-10-27. Confirmed on Microsoft Learn: overview-inbound-outbound-ips (possible outbound addresses, Premium v4 has no stable outbound IPs),
nat-gateway-integration (64,512 SNAT ports per IP, up to 16 IPs, NAT gateway on the integration subnet mitigates SNAT exhaustion), overview-vnet-integration (route all),
troubleshoot-intermittent-outbound-connection-errors, overview-diagnostics (SNAT in diagnostics).
Removed: the 128-port default, tier-family change list, `--idle-timeout 10` example value, NAT zonal statement, Functions Consumption statement, exception names.

Method: documentation only; no commands were run.
