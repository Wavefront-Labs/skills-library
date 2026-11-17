---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-hybrid-connections
name: app-service-hybrid-connections
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service-networking, hybrid-connections, relay, hybrid-connection-manager, on-premises-access]
level: practitioner
status: docs-checked
description: "Reach a single on-prem host:port from App Service without VPN using Hybrid Connections: Relay namespace, Hybrid Connection Manager install, HA, limits and troubleshooting."
sources: ["https://learn.microsoft.com/azure/app-service/app-service-hybrid-connections", "https://learn.microsoft.com/azure/azure-relay/relay-hybrid-connections-protocol"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Service Hybrid Connections

**Goal:** an App Service or Function calls an on-prem endpoint (SQL Server, an internal API)
quickly, outbound-only from on-prem, with no VPN or firewall inbound rules.

## How it works
App → Azure Relay hybrid connection (443) ← **Hybrid Connection Manager (HCM)** on-prem (outbound 443)
→ target `host:port`. Each hybrid connection maps one `host:port` (TCP only). The app connects
to that exact hostname and port as if local; App Service intercepts DNS for it.

## Set up
1. App Service → Networking → Hybrid connections → Add → create new: name, endpoint host (as the app will call it, e.g. `sql01.corp.local`), port `1433`, Relay namespace.
   CLI: `az webapp hybrid-connection add -g rg -n app-orders --namespace relay-hc --hybrid-connection hc-sql01`.
2. Install **HCM** on a Windows Server (or the Linux HCM, which runs on Windows and Linux) that can resolve and reach the target. Sign in → select the hybrid connections → status *Connected*.
3. HA: install HCM on a second server with the same connections — load-balanced automatically.

## Limits and fit
| Plan | Hybrid connections |
|---|---|
| Basic | 5 per plan |
| Standard | 25 per plan |
| Premium (v1-v4) | 220 per app |
| Isolated v2 | 220 per app |
- TCP only, fixed host:port: no UDP, no TCP services on dynamic ports (such as FTP passive mode), no LDAP (it can need UDP). Not supported for Windows custom containers.
- Billing is per the Azure Relay pricing page.

## Troubleshooting
- Kudu console: `tcpping sql01.corp.local:1433` — success means the relay path works.
- The HCM UI shows connection states.
- Proxy on-prem: HCM connects outbound to Azure Relay; configure the system proxy if needed.
- Name mismatch: the app must use the exact endpoint hostname configured, not an IP or FQDN variant.

## Gotchas
- Not a security boundary for lateral movement: the HCM host can reach anything; restrict its network.
- Use VNet integration + S2S VPN/ExpressRoute instead when many endpoints or high throughput are involved.

## Verify
- [ ] Portal shows the connection *Connected* with ≥ 2 HCM instances.
- [ ] `tcpping` from Kudu succeeds; app health check exercising the dependency is green.

## Checked

2026-10-28. Confirmed on the App Service Hybrid Connections page: limits Basic 5 per plan, Standard 25 per plan, Premium v1-v4 and Isolated v2 220 per app; no UDP, no dynamic-port TCP services, no LDAP; HCM runs on Windows and Linux; not supported for Windows custom containers. Fixed: the 220 limit is per app, not per plan. Removed: the Relay tier requirement, the HCM status cmdlet and CLI names, the service bus host name, the SAS rotation claim and billing detail.

Method: documentation only; no commands were run.
