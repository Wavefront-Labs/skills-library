---
id: computing-software.cloud-infrastructure-engineering.azure.azure-firewall-troubleshooting-with-policy-analytics-and-logs
name: azure-firewall-troubleshooting-with-policy-analytics-and-logs
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-firewall, firewall-troubleshooting, policy-analytics, azfw-logs, rule-processing, fat-flows]
level: advanced
status: gated
description: "Find why Azure Firewall dropped (or allowed) traffic: rule processing order, structured AZFW* logs, policy analytics for rule hits and unused rules, and common misconfigurations."
sources: ["https://learn.microsoft.com/azure/firewall/policy-analytics", "https://learn.microsoft.com/azure/firewall/firewall-structured-logs", "https://learn.microsoft.com/azure/firewall/rule-processing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Firewall troubleshooting

**Goal:** answer "is the firewall blocking this?" with log evidence, and keep the rule base lean.

## Processing order (policy)
Threat-intelligence filtering, when enabled, is processed first, before network and application rules. Rule collection
groups are processed in priority order; within the policy, DNAT rules, then network rules, then application rules.
When a policy inherits from a parent, the parent's rule collection groups always take precedence regardless of the
child's priority numbers. Application rules are evaluated only when no network rule matched and the protocol is HTTP,
HTTPS or MSSQL; for HTTPS the match uses SNI only. Application rules do not apply to inbound connections (use WAF
for inbound HTTP/S filtering). IDPS in Alert mode runs in parallel with rule processing.

## Structured logs
Enable resource-specific (structured) logs to a Log Analytics workspace; the AZFWNATRule table logs only when a DNAT
rule matches (no match, no entry). The Top Flows (Fat Flows) log shows the connections with the highest throughput.
Network, application, DNS proxy, threat intelligence and IDPS logs also exist. Table and column names used below
(AZFWNetworkRule, AZFWApplicationRule, Action, Rule, ...) were not visible in the fetched page text
(gated: unconfirmed, source is paywalled or blocked); look them up in the firewall monitoring data reference first.
```kusto
union AZFWNetworkRule, AZFWApplicationRule
| where TimeGenerated > ago(30m)
| where SourceIp == "10.20.1.4"
| order by TimeGenerated desc
```
No log line for a flow you expected suggests traffic never reached the firewall (routing/UDR problem).

## Policy analytics (Firewall Manager)
Enable it on the policy and choose a Log Analytics workspace, which must be the same workspace as in the firewall's
diagnostic settings. It depends on Log Analytics and resource-specific logging. Features: rule analytics (finds
low-use rules), traffic-flow insights and single-rule analysis. Use it periodically to remove stale rules.

## Common causes
- **Asymmetric routing**: return path bypasses the firewall (spoke missing UDR).
- Protocols other than HTTP/HTTPS/MSSQL need network rules, not application rules.
- HTTPS clients that send no SNI cannot match FQDN application rules.
- Check the destination's NSG as well as the firewall.

## Verify
- [ ] Flow appears with the expected action after the fix; policy analytics shows the rule hit; stale rules reviewed.

## Checked
2026-10-28. Confirmed (Learn: firewall/rule-processing, policy-analytics, firewall-structured-logs): processing order,
threat intel first, parent-over-child precedence, HTTP/HTTPS/MSSQL and SNI behaviour, no application rules inbound, IDPS
alert parallelism, AZFWNATRule logging behaviour, Fat Flows log, policy analytics workspace dependency and features.
Removed (unconfirmed): AZFWFatFlow/AZFWDnsQuery/AZFWIdpsSignature/AZFWThreatIntel table names, "FQDN in network rules
needs DNS proxy", DNAT/NSG rule, TLS-inspection and IDPS Deny bullets, log-lag and rule-apply timings. Gated: the KQL
table and column names.
Method: documentation only; no commands were run.
