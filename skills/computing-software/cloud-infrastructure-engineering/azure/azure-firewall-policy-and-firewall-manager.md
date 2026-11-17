---
id: computing-software.cloud-infrastructure-engineering.azure.azure-firewall-policy-and-firewall-manager
name: azure-firewall-policy-and-firewall-manager
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-firewall, azure-firewall-policy, firewall-manager, rule-collection-groups, network-rules, application-rules, dnat, fqdn-tags, fqdn-filtering, ip-groups, dns-proxy, threat-intelligence, idps, tls-inspection, firewall-premium, firewall-basic, forced-tunnelling, hub-firewall, secured-virtual-hub, firewall-logs, structured-logs, egress-control, web-categories, firewall-deploy, firewall-sku, azurefirewallsubnet]
level: advanced
status: docs-checked
description: "Operate Azure Firewall: policy hierarchy, rule collection groups, network/application/DNAT rules, IP groups, FQDN tags, DNS proxy, Premium IDPS and TLS inspection, log triage."
sources: ["https://learn.microsoft.com/en-us/azure/firewall/rule-processing", "https://learn.microsoft.com/en-us/azure/firewall/policy-rule-sets", "https://learn.microsoft.com/en-us/azure/firewall/premium-features", "https://learn.microsoft.com/en-us/azure/firewall/premium-certificates", "https://learn.microsoft.com/en-us/azure/firewall/dns-settings", "https://learn.microsoft.com/en-us/azure/firewall/snat-private-range", "https://learn.microsoft.com/en-us/azure/firewall/forced-tunneling", "https://learn.microsoft.com/en-us/azure/firewall/monitor-firewall-reference", "https://learn.microsoft.com/en-us/azure/firewall/firewall-faq", "https://learn.microsoft.com/en-us/azure/firewall-manager/overview"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Azure Firewall — hub policy, rule collections and the logs that explain a drop

**Goal:** every spoke's egress goes through a firewall whose rules live in a policy
hierarchy you can read, with FQDN-level allow lists, DNS proxy so FQDN rules actually
work, and logs that answer "why was this blocked" in one query.

## 1. Deploy
```bash
az network vnet subnet create -g rg-hub --vnet-name vnet-hub -n AzureFirewallSubnet --address-prefixes 10.0.0.0/26   # exact name; size per the firewall FAQ
az network vnet subnet create ... -n AzureFirewallManagementSubnet --address-prefixes 10.0.0.64/26               # Management NIC subnet, for forced tunnelling
az network public-ip create -g rg-hub -n pip-fw --sku Standard --zone 1 2 3
az network firewall policy create -g rg-hub -n fwp-parent --sku Premium --threat-intel-mode Deny --enable-dns-proxy true
az network firewall policy create -g rg-hub -n fwp-prod --base-policy fwp-parent --sku Premium
az network firewall create -g rg-hub -n fw-hub --sku AZFW_VNet --tier Premium --firewall-policy fwp-prod --vnet-name vnet-hub --public-ip pip-fw --conf-name fw-ipconfig
```
- Tiers: **Basic**, **Standard**, **Premium** (TLS inspection, IDPS, URL filtering, web categories); the policy SKU must match the firewall tier.
- For new deployments the FAQ says to omit availability zones (`--zones`): Azure manages zone allocation in zone-redundant regions.
- Spokes: UDR `0.0.0.0/0 → VirtualAppliance <fw private IP>` on every subnet
  (+ `AzureFirewallSubnet` route to Internet for its own egress); disable BGP propagation
  on spoke route tables when ExpressRoute would otherwise inject a default route.
- Forced tunnelling (default route to on-prem) needs the Management NIC; DNAT isn't supported with forced tunnelling.

## 2. Policy hierarchy and rule order
Parent (org-wide: deny known-bad, allow platform FQDNs, threat intel) → child policies
(per environment/landing zone) inherit parent rules which are evaluated **first**.
Within a policy: **Rule collection groups** (priority 100–65000) → **rule collections**
(priority, action Allow/Deny, type) → rules.
Processing order (regardless of priority across types): **DNAT → Network → Application**.
A network rule that allows `TCP 443 to *` makes every application rule moot — keep
network rules to non-HTTP (NTP, SQL 1433, DNS) and specific destinations, and do HTTP(S)
egress via application rules with FQDNs.
```bash
az network firewall policy rule-collection-group create -g rg-hub --policy-name fwp-prod -n rcg-egress --priority 300
az network ip-group create -g rg-hub -n ipg-spokes --ip-addresses 10.1.0.0/16 10.2.0.0/16
az network firewall policy rule-collection-group collection add-filter-collection -g rg-hub --policy-name fwp-prod --rcg-name rcg-egress \
  -n app-allow-updates --collection-priority 200 --action Allow --rule-type ApplicationRule \
  --rule-name win-update --source-ip-groups ipg-spokes --fqdn-tags WindowsUpdate AzureKubernetesService
az network firewall policy rule-collection-group collection rule add ... --collection-name app-allow-updates -n pypi --rule-type ApplicationRule \
  --source-ip-groups ipg-spokes --protocols Https=443 --target-fqdns pypi.org files.pythonhosted.org "*.github.com"
az network firewall policy rule-collection-group collection add-filter-collection ... -n net-allow --rule-type NetworkRule --action Allow --collection-priority 100 \
  --rule-name ntp --source-ip-groups ipg-spokes --dest-addr "*" --destination-ports 123 --ip-protocols UDP
az network firewall policy rule-collection-group collection add-nat-collection ... -n dnat-rdp --collection-priority 100 \
  --rule-name web --source-addresses 203.0.113.0/24 --destination-addresses <fw-public-ip> --destination-ports 443 --translated-address 10.1.2.4 --translated-port 443 --ip-protocols TCP
```
- **IP Groups** for sources/destinations (reusable, updated without touching rules).
- **FQDN tags** (e.g. `WindowsUpdate`, `AzureKubernetesService`; list them with the firewall FQDN tag docs), **service tags** in network rules (`Storage.UKSouth`, `Sql`),
  **web categories** (Premium/Standard subset) for "allow news, deny gambling".
- FQDNs in **network** rules (for non-HTTP to a hostname) and FQDN filtering in application rules both require **DNS proxy** enabled and spokes using the firewall as DNS (VNet DNS = firewall private IP) — otherwise the firewall and the client may resolve differently and the rule misses.
- Explicit deny-all collection at the lowest priority with logging makes the implicit drop visible and named.

## 3. Premium features
- **TLS inspection**: an intermediate CA certificate stored in Key Vault as a password-less PFX (PEM isn't supported); the firewall's identity must be able to read the secret; enable inspection on the application rules; clients must trust the CA. Exclude pinned apps (Windows Update, banking) via rules without inspection.
- **IDPS**: signature modes Disabled, Alert, or Alert and Deny; bypass list for noisy internal scanners; private IP ranges define "internal" for traffic direction.
- **URL filtering** (the whole URL including path) and web categories.
- SNAT: no SNAT to destinations in IANA RFC 1918 / RFC 6598 private ranges; to change that, set private ranges (the CLI `--private-ranges` applies only to classic rules; with a policy use ARM template or portal) or enable auto-learn SNAT routes.

## 4. Logs
Diagnostic settings → **resource-specific** tables (`AZFWNetworkRule`, `AZFWApplicationRule`,
`AZFWNatRule`, `AZFWDnsQuery`, `AZFWIdpsSignature`, `AZFWThreatIntel`, `AZFWFlowTrace`) — pick *Resource specific*, not AzureDiagnostics.
```kusto
AZFWApplicationRule | where Action == "Deny" and TimeGenerated > ago(1h)
| summarize count() by SourceIp, Fqdn, Protocol, RuleCollection, Rule | order by count_ desc
```
`AZFWNetworkRule | where Action == "Deny"` for non-HTTP; `AZFWDnsQuery` to see what clients resolve. Alert on Deny spikes from a single source and on `AZFWThreatIntel` hits.
Metrics: `Throughput`, `SNAT port utilization` (more public IPs add SNAT ports; up to 250 per firewall in a VNet, 2,496 ports per IP per instance), `Firewall health state`, `Latency Probe`.

## 5. Firewall Manager
Central view across firewalls and secured virtual hubs; associates policies to hubs/VNets,
manages **secured virtual hubs** (Virtual WAN + Azure Firewall with routing intent),
and DDoS protection plan association.
In hub-and-spoke VNets it's mostly a policy-association UI; in vWAN it's where routing intent (`Internet` / `Private` traffic via firewall) is set.

## Gotchas
- Rules are processed by type (DNAT, then network, then application) regardless of priority, and rule collection groups of a parent policy always take precedence over the child's.
- Destination `*` in network rules on port 443 silently bypasses all FQDN governance — the most common misconfiguration in a "secure" hub.
- DNS proxy off + FQDN rules = intermittent allow/deny depending on DNS round-robin answers.
- Asymmetric routing: return traffic from on-prem to Azure must also pass the firewall (ExpressRoute/GatewaySubnet UDRs for spoke ranges → firewall), or stateful inspection drops it.
- A firewall is billed while deployed; see the Azure Firewall pricing page before leaving dev firewalls running.

## Checked
2026-10-28. Confirmed on Microsoft Learn (Azure Firewall rule processing, policy rule sets, Premium features and certificates, DNS settings, SNAT private ranges, forced tunnelling, monitor reference, FAQ, Firewall Manager overview): rule collection priority 100-65,000, DNAT then network then application order, parent-policy precedence, DNS proxy requirement for FQDNs in network rules, intermediate CA in Key Vault as PFX, IDPS modes, resource-specific log tables, metric names, up to 250 public IPs, 2,496 SNAT ports per IP per instance, SNAT ranges (RFC 1918/6598), forced tunnelling and DNAT. Corrected: `--zones` (FAQ says omit), `--private-ranges` applies to classic rules only, parent/child precedence gotcha. Removed: subnet size, upgrade-in-place, FQDN tag list, SNAT utilisation threshold, apply-time, deallocate/billing and partner claims.
Method: documentation only; no commands were run.

## Verify
- [ ] From a spoke VM: `curl https://pypi.org` works, `curl https://example.org` is denied; `AZFWApplicationRule` shows both with the matching rule name within minutes.
- [ ] `nslookup` from the spoke resolves via the firewall (`AZFWDnsQuery` logs the query).
- [ ] `az network nic show-effective-route-table` on spoke NICs shows `0.0.0.0/0 → <fw IP>`; traceroute first hop is the firewall.
- [ ] SNAT port utilisation has headroom at peak; Firewall health state 100.
