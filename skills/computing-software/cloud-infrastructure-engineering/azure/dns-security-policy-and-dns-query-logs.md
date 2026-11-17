---
id: computing-software.cloud-infrastructure-engineering.azure.dns-security-policy-and-dns-query-logs
name: dns-security-policy-and-dns-query-logs
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-dns, dns-security-policy, dns-query-logs, domain-lists, dns-filtering, threat-protection]
level: advanced
status: docs-checked
description: "Filter and log VNet DNS queries with Azure DNS security policy: domain lists, block/allow/alert rules, VNet links, and sending query logs to Log Analytics."
sources: ["https://learn.microsoft.com/azure/dns/dns-security-policy", "https://learn.microsoft.com/azure/dns/dns-security-policy-quickstart", "https://learn.microsoft.com/azure/firewall/dns-settings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS security policy and DNS query logs

**Goal:** see every DNS query workloads make, and block known-bad or unapproved domains at resolution time.

## Building blocks
- **DNS security policy** (resolver policy): regional resource; it can only be linked to VNets in the same region.
- **Domain lists**: sets of domains.
- **Security rules**: priority + domain list(s) + action **Allow**, **Block** (answer with a block response) or
  **Alert** (log only).
- **Virtual network links**: attach the policy to VNets (one policy per VNet; one policy can link many VNets in its region).
- **Diagnostic settings** on the policy: DNS query logs to Log Analytics, storage or Event Hubs.

## Rollout
1. Create the policy and link to VNets with a single **Alert** rule for a broad list (or none) and enable query logs -
   gives visibility without risk.
2. Analyse queries: top domains per source, NXDOMAIN rates, unexpected external domains (exfiltration via DNS).
3. Add Block rules for threat-intel domain lists and policy-violating domains; keep an Allow rule with higher
   priority for exceptions.
Create via portal or CLI/Bicep; look up the current resource types and CLI commands in the DNS security policy quickstart.

## Query
Query the log destination you chose in the diagnostic setting; inspect the table and columns with `| take 10` before writing summaries (names not confirmed here).

## Alternatives / complements
- Azure Firewall **DNS proxy** with FQDN filtering logs queries passing through the firewall.
- Defender for DNS / Defender for Servers alert on suspicious resolution patterns.

## Gotchas
- Policies apply to queries from linked VNets resolved through Azure DNS; VMs using custom DNS
  servers elsewhere bypass it unless those servers forward through a linked VNet.
- Overly broad block lists break Azure service endpoints (e.g. blocking `*.windows.net`) - test.

## Verify
- [ ] Query logs arrive for linked VNets; resolving a blocked test domain returns the block response and is logged.

## Checked

2026-10-28. Confirmed on the DNS security policy page: policy is regional and links only to VNets in its region, one policy per VNet, rule actions Allow, Block and Alert. Removed: resource type names, the log table query, the Firewall log table name and the Azure DNS virtual IP (not found in fetched pages).

Method: documentation only; no commands were run.
