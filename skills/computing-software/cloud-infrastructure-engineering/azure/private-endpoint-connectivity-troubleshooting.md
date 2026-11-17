---
id: computing-software.cloud-infrastructure-engineering.azure.private-endpoint-connectivity-troubleshooting
name: private-endpoint-connectivity-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, private-link, private-endpoint-troubleshooting, dns, asymmetric-routing, connection-troubleshoot]
level: practitioner
status: docs-checked
description: "Debug private endpoint access: connection state, DNS answers against the privatelink zone, and NSG/UDR behaviour with subnet network policies."
sources: ["https://learn.microsoft.com/azure/private-link/private-endpoint-dns", "https://learn.microsoft.com/azure/private-link/disable-private-endpoint-network-policy", "https://learn.microsoft.com/cli/azure/network/private-endpoint", "https://learn.microsoft.com/cli/azure/network/watcher"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private endpoint connectivity troubleshooting

**Goal:** a repeatable checklist for "it works publicly but not via the private endpoint" (or vice versa).

## 1. Connection state
```bash
az network private-endpoint show -g rg -n pe-sql --query "{state:privateLinkServiceConnections[0].privateLinkServiceConnectionState.status,ip:customDnsConfigs}"
```
Confirm the connection is approved; if not, fix that before looking at DNS or routing.

## 2. DNS from the client
```bash
nslookup sqlsrv.database.windows.net
```
Azure puts a CNAME on public DNS that redirects to the private domain name; a private DNS zone linked to the client's
virtual network overrides that with the endpoint's private IP. For Azure SQL Database the private zone is
`privatelink.database.windows.net` and the public forwarder zone is `database.windows.net`. A public IP in the answer
means the zone is not linked to the client's network, the client uses DNS that cannot see the zone, or the A record is
missing. Do not share one private zone's records between endpoints of different services: it can delete the first
A record (Private endpoint DNS page).

## 3. Network path
- Test the TCP port from the client, then run Network Watcher connection troubleshoot from a VM:
```bash
az network watcher test-connectivity -g rg --source-resource vm-client --dest-address sqlsrv.database.windows.net --dest-port 1433
```
- Network policies are disabled by default on a subnet. NSG and user-defined route support for private endpoints
  applies only when network policy support is enabled on that subnet (NSGs, route tables, or both), and the setting
  affects all private endpoints in the subnet.

## 4. On-prem clients
The DNS page lists, per service, the private zone name and the public zone to forward; forward that public zone from
on-prem DNS to a resolver that can see the linked private zone.

## Verify
- [ ] Private IP returned in DNS and TCP connect succeeds from the client.

## Checked
2026-11-01. Confirmed in Private endpoint DNS configuration (CNAME redirect, private zone override, SQL zone names,
one zone per service, public forwarder column), Manage network policies for private endpoints (default disabled,
NSG/UDR only when enabled, subnet-wide), and the az reference pages (command and flags). The
troubleshooting page named in the old sources returned 404, so it was dropped. Removed: connection status names,
TLS name-mismatch claim, asymmetric routing/SNAT advice, service-side sub-resource list, logs claim.
Method: documentation only; no commands were run.
