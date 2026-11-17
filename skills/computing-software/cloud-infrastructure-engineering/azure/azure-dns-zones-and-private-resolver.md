---
id: computing-software.cloud-infrastructure-engineering.azure.azure-dns-zones-and-private-resolver
name: azure-dns-zones-and-private-resolver
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-dns, dns-zones, public-dns-zones, private-dns-zones, dns-private-resolver, alias-records, vnet-links, auto-registration, dns-forwarding-ruleset, inbound-endpoint, outbound-endpoint, conditional-forwarding, hybrid-dns, privatelink-zones, split-horizon, dnssec, dns-delegation, azure-provided-dns, 168-63-129-16]
level: practitioner
status: docs-checked
description: "Design Azure DNS: public zones with alias records and DNSSEC, private zones with VNet links and auto-registration, privatelink zones, and Private Resolver for hybrid forwarding."
sources: ["https://learn.microsoft.com/en-us/azure/dns/dns-alias", "https://learn.microsoft.com/en-us/azure/dns/private-dns-virtual-network-links", "https://learn.microsoft.com/en-us/azure/dns/dns-private-resolver-overview", "https://learn.microsoft.com/en-us/azure/dns/private-resolver-endpoints-rulesets", "https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns-integration", "https://learn.microsoft.com/en-us/azure/dns/dnssec", "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits", "https://learn.microsoft.com/en-us/cli/azure/dns-resolver"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure DNS — public zones, private zones and hybrid resolution that scales

**Goal:** names resolve correctly from Azure, on-prem and the internet; every private
endpoint gets its record automatically; no VM is pointed at a hand-built DNS server.

## 1. Public zones
```bash
az network dns zone create -g rg-dns -n example.com      # set the zone's NS names at the registrar
az network dns record-set a add-record -g rg-dns -z example.com -n www -a 203.0.113.10 --ttl 300
az network dns record-set a create -g rg-dns -z example.com -n apex --target-resource <public-ip-or-traffic-manager-id>   # alias record
az network dns dnssec-config create -g rg-dns -z example.com; az network dns record-set ds ... # publish DS at registrar
```
- **Alias records** (A/AAAA/CNAME → Standard public IP, Traffic Manager, CDN endpoint, Front Door endpoint, or another record set of the same type) track the target's changes. For new Traffic Manager setups the docs suggest Traffic Manager Linked Records instead.
- Delegate subzones (`az network dns record-set ns`) to other teams/subscriptions.
- Import/export BIND files: `az network dns zone import/export`.

## 2. Private zones
```bash
az network private-dns zone create -g rg-dns -n corp.internal
az network private-dns link vnet create -g rg-dns -z corp.internal -n hub -v <hub-vnet-id> --registration-enabled false
az network private-dns link vnet create -g rg-dns -z corp.internal -n spoke1 -v <spoke-id> --registration-enabled true   # VMs auto-register A records
```
- **Auto-registration**: one registration link per VNet (VNet ↔ one zone); resolution links up to 1000 per zone (a VNet can link to up to 1000 private zones).
- Azure-provided DNS (`168.63.129.16`) resolves private zones linked to the VNet the
  query comes from; VNet DNS settings stay *Default*. If you must set custom DNS on a
  VNet (on-prem AD), those servers need to forward Azure names to the Private Resolver.
- **Private Link zones** (`privatelink.blob.core.windows.net`, `privatelink.database.windows.net`,
  `privatelink.vaultcore.azure.net`, …): create once in the hub/connectivity subscription,
  link to **every** VNet, and let Policy `DeployIfNotExists` (*Configure private DNS zones for private endpoints* initiative)
  create the A record via the private endpoint's `privateDnsZoneGroup`. Never let spokes create their own copies — split-brain.
- Split-horizon: `app.example.com` public → Front Door; private zone `example.com` with
  `app` → private endpoint; VNet-linked clients get the private answer. Beware: a private
  zone for `example.com` hides every other public record unless you replicate them.

## 3. DNS Private Resolver (hybrid)
```bash
az extension add -n dns-resolver
az dns-resolver create -g rg-dns -n dnspr-hub -l uksouth --id <hub-vnet-id>
az dns-resolver inbound-endpoint create -g rg-dns --dns-resolver-name dnspr-hub -n inbound -l uksouth --ip-configurations '[{"private-ip-allocation-method":"Dynamic","id":"<snet-dns-in>"}]'   # subnet delegated to Microsoft.Network/dnsResolvers, /28 to /24
az dns-resolver outbound-endpoint create -g rg-dns --dns-resolver-name dnspr-hub -n outbound -l uksouth --id <snet-dns-out>
az dns-resolver forwarding-ruleset create -g rg-dns -n rs-hub -l uksouth --outbound-endpoints '[{"id":"<out-ep-id>"}]'
az dns-resolver forwarding-rule create -g rg-dns --ruleset-name rs-hub -n corp --domain-name corp.example.com. --forwarding-rule-state Enabled --target-dns-servers '[{"ip-address":"10.50.0.4","port":53}]'
az dns-resolver vnet-link create -g rg-dns --ruleset-name rs-hub -n spoke1 --id <spoke-vnet-id>
```
- **Inbound endpoint** IP = what on-prem DNS **conditional-forwards** Azure private zones and
  private-endpoint names to. Forward the public zone name (`blob.core.windows.net`, `database.windows.net`), not the `privatelink.` name, as the Private Link DNS page instructs. Replaces DNS forwarder VMs.
- **Outbound endpoint + ruleset**: Azure-side queries for `corp.example.com` go to on-prem
  DCs; link the ruleset to each spoke VNet (or just the hub if spokes use hub resolution).
  A wildcard rule `.` forwards everything unresolved — use carefully.
- Keep VNet DNS = Azure default so the resolver's own links apply; a ruleset link is
  the "custom DNS" replacement.
- Limits: 5 inbound and 5 outbound endpoints per resolver, 1 resolver per VNet, 1000 forwarding rules per ruleset, 500 VNet links per ruleset, 10,000 QPS per endpoint.

## 4. On-prem and AD
AD-joined Azure VMs that must use DCs for DNS: set VNet DNS to DCs, and on the DCs
conditional-forward Azure private zones to the inbound endpoint — both directions, or
private endpoints won't resolve from AD-DNS clients and `168.63.129.16` must remain
reachable for the agent (it's a platform dependency regardless of DNS settings).

## Gotchas
- A VM's NIC-level DNS overrides VNet DNS; `az network nic show --query dnsSettings` when one box behaves differently.
- Private zone names that collide with public (`example.com`) make public records for that domain invisible inside Azure; use a dedicated private suffix (`corp.internal`) where you can.
- Each Private Resolver endpoint needs its own subnet delegated to `Microsoft.Network/dnsResolvers`, used for nothing else.
- Policy-driven privatelink records need the private endpoint to carry a `privateDnsZoneGroup` (`dns-zone-group`); without one, no record is created.
- Public DNSSEC: publish the DS record in the parent zone (at the registrar); without it, validating resolvers treat the child zone as insecure.

## Checked
2026-10-28. Confirmed on Microsoft Learn (Azure DNS alias records, DNSSEC, Private DNS virtual network links, DNS Private Resolver overview and endpoints/rulesets, Private Link DNS integration, subscription and service limits, `az dns-resolver` references): alias targets, one auto-registration zone per VNet, 1000 links per zone, resolver limits (5 inbound, 5 outbound, 1000 rules, 500 ruleset links, 10,000 QPS), subnet delegation and /28-/24 size, conditional forwarding to public zone names, DS record behaviour, command names and flags. Corrected: the resolver commands are the `az dns-resolver` extension group, not under `az network`; endpoint limit (was 20); forwarding to `privatelink.` names. Removed: RBAC/Policy remarks, NIC-detach and registrar-window claims.
Method: documentation only; no commands were run.

## Verify
- [ ] `dig +short www.example.com @8.8.8.8` returns the alias target; `delv example.com` validates DNSSEC (if enabled).
- [ ] From a spoke VM: `nslookup stprod.blob.core.windows.net` → `10.x` private IP; from on-prem the same via the inbound endpoint.
- [ ] From a spoke VM: `nslookup dc01.corp.example.com` resolves through the outbound ruleset (resolver metrics show queries).
- [ ] Policy compliance for *private DNS zone groups* is 100 % in production subscriptions.
