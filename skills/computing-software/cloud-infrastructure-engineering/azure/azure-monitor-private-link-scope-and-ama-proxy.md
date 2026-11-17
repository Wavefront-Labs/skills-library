---
id: computing-software.cloud-infrastructure-engineering.azure.azure-monitor-private-link-scope-and-ama-proxy
name: azure-monitor-private-link-scope-and-ama-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-monitor-agent, ampls, monitor-private-link-scope, ama-proxy, private-endpoint, data-collection-endpoint]
level: advanced
status: docs-checked
description: "Send monitoring data privately with Azure Monitor Private Link Scope (AMPLS): access modes, DNS, data collection endpoints, and AMA proxy settings for restricted egress."
sources: ["https://learn.microsoft.com/azure/azure-monitor/logs/private-link-security", "https://learn.microsoft.com/azure/azure-monitor/logs/private-link-design", "https://learn.microsoft.com/azure/azure-monitor/agents/azure-monitor-agent-network-configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMPLS and AMA proxy configuration

**Goal:** agents and apps send logs/metrics to Azure Monitor without public internet, or through a mandated proxy.

## AMPLS model
- An **Azure Monitor Private Link Scope** groups Log Analytics workspaces, Application Insights components and **data collection endpoints (DCEs)**; a virtual network can connect to only one AMPLS, so that AMPLS must cover every Azure Monitor resource the network needs.
- Azure Monitor endpoints are shared global/regional DNS names. Connecting a network to an AMPLS updates DNS for every network that shares that DNS, not just the connected one.
- Therefore: **one AMPLS per DNS boundary**. Peered networks most likely share DNS, so create a single private link reachable from all of them; only the last private endpoint set in DNS applies. Networks that are not peered must also have separate DNS before they can each have their own AMPLS.

## Access modes
| Setting | `Open` | `PrivateOnly` |
|---|---|---|
| Reaches resources in the AMPLS | Yes | Yes |
| Reaches resources outside the AMPLS | Yes | No (prevents data exfiltration) |
Ingestion and queries each have their own access mode setting, and modes can apply to all connected networks or to specific ones (for example Private Only for ingestion and Open for queries). Start with **Open** while onboarding so resources not yet in the scope keep working, then move to Private Only.

## Steps
1. Create AMPLS; add workspaces, Application Insights components and the DCE(s) used by AMA DCRs.
2. Create the AMPLS private endpoint in the network and let it create the private DNS zones (see the AMPLS configuration page for the zone list).
3. AMA with AMPLS: all DCRs must use DCEs, and those DCEs must be added to the scope. With private links, add only private DCEs; the agent does not use the non-private endpoints.
4. Validate DNS from a VM: `nslookup <workspaceId>.ods.opinsights.azure.com` should resolve to a private IP.

## AMA proxy
Set via extension settings (Windows and Linux), protected settings carry credentials:
```bash
az vm extension set -g rg --vm-name vm1 -n AzureMonitorLinuxAgent --publisher Microsoft.Azure.Monitor \
  --settings '{"proxy":{"mode":"application","address":"http://proxy.example.com:3128","auth":"true"}}' \
  --protected-settings '{"proxy":{"username":"svc","password":"<secret>"}}'
```
Both anonymous and basic (username/password) proxy authentication are supported; Arc-enabled servers do not support the Log Analytics (OMS) gateway. Proxy settings do not apply to Azure Monitor Metrics (preview) as a destination.
Without AMPLS, firewalls must allow outbound 443 (with HTTPS inspection disabled) to: `global.handler.control.monitor.azure.com`, `<region>.handler.control.monitor.azure.com`, `global.prod.microsoftmetrics.com`, `<workspaceId>.ods.opinsights.azure.com` and `<dce>.<region>.ingest.monitor.azure.com`; `management.azure.com` and `<region>.monitoring.azure.com` only for custom metrics. Enable both the `AzureMonitor` and `AzureResourceManager` service tags; service tags do not include DCE public IPs.

## Verify
- [ ] `Heartbeat | where Computer == "vm1"` is fresh and the DNS check resolves privately.
- [ ] The agent's extension logs show no connection errors to the endpoints above.

## Checked
2026-10-28. Confirmed on the Azure Monitor private link design, private link security and AMA network configuration pages: one AMPLS per shared DNS, one AMPLS per virtual network, Open versus Private Only and separate ingestion/query settings, DCEs required with AMPLS and private DCEs only, proxy modes and `none`/`application` settings with `address` and `auth`, firewall endpoint list, port 443, HTTPS inspection, required service tags, Arc/OMS gateway note. CLI flags checked with check_commands. Removed: private DNS zone names and endpoint-group name, workspace public-access toggle wording, same-region DCE rule, association command, log file paths.
Method: documentation only; no commands were run.
