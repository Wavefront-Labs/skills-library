---
id: computing-software.cybersecurity-defensive.network-defence.firewall-rule-cleanup
name: firewall-rule-cleanup
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [firewall, rule-cleanup, shadowed-rules, unused-rules, hit-counts, policy-optimizer, any-any-rules, rulebase-hygiene]
level: practitioner
status: draft
description: "Clean up a bloated firewall rulebase safely: find unused, shadowed, redundant and overly broad rules with hit counts and analysis tools, disable-then-delete, and keep it clean."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/app-id/security-policy-rule-optimization", "https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/", "https://csrc.nist.gov/pubs/sp/800/41/r1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Firewall rule cleanup

Old rulebases accumulate thousands of rules nobody understands. Unused and broad rules are attack
surface; shadowed rules hide intent; size slows reviews and changes.

## Categories to find
- **Unused**: zero hits over a long enough period (cover quarterly/annual jobs: use 6-12 months).
- **Shadowed**: never matched because an earlier rule matches the same traffic.
- **Redundant**: duplicates or subsets of other rules with the same action.
- **Overly permissive**: any source/destination/service, large ranges, "any" application on NGFW.
- **Expired/temporary**: rules for finished projects (if you tagged them, easy).
- **Orphaned objects**: address/service objects not referenced.

## Data sources
- Hit counts: Palo Alto (`show rule-hit-count vsys vsys-name vsys1 rule-base security rules all`,
  Policy Optimizer: rules without App-ID, unused apps, unused rules), FortiGate (Policy & Objects hit
  count and last used), Check Point (hit count column), Cisco ASA (`show access-list` hitcnt).
- Ensure hit counters were not reset recently (reboots, upgrades, HA failover can reset on some platforms).
- Analysis tools: Tufin, AlgoSec, FireMon, Skybox, or open-source Batfish/Capirca for shadowing analysis.

## Safe process
1. Export the rulebase and hit data; identify candidates with owner and ticket references.
2. Contact owners (rule descriptions/tags should name them; if not, use the change history).
3. **Disable** candidate rules (not delete), log the change, wait one business cycle (30-90 days).
   Enable logging on the cleanup/deny rule to see what breaks.
4. Delete disabled rules with no complaints; remove orphaned objects.
5. Tighten broad rules using traffic logs: replace `any` service with observed ports, App-ID based
   rules from Policy Optimizer suggestions.

## Keep it clean
- Every rule has owner, ticket, and expiry (tags or description convention) enforced at change time.
- Quarterly unused-rule report; annual recertification by owners.
- Reject new any-any requests by policy.

## Gotchas
- Disaster recovery and seasonal flows have zero hits for months; ask before deleting.
- HA pairs and multiple firewalls: hits must be summed across all members.
- Rules referenced by NAT or PBR may look unused in security policy reports.

## Verify
Rule count, any-any count, and unused count trend down quarter on quarter, with no outage tickets
traced to the cleanup.
