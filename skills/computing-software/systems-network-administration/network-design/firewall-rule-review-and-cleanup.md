---
id: computing-software.systems-network-administration.network-design.firewall-rule-review-and-cleanup
name: firewall-rule-review-and-cleanup
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, firewall, firewall-rules, firewall-rule-review, shadowed-rules, redundant-rules, zero-hit-rules, rule-recertification, rule-cleanup, hit-counters, policy-optimizer, compliance-audit]
level: practitioner
status: docs-checked
description: "Run a periodic firewall rule review: export and hit counts, finding unused, shadowed, redundant and over-permissive rules, owner recertification, safe disable-then-delete cleanup."
sources:
  - https://csrc.nist.gov/pubs/sp/800/41/r1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall rule review and cleanup

Rule bases grow monotonically unless someone removes rules. Review rule sets on a fixed schedule
set by your policy and any compliance regime.

## 1. Gather data
- Export the policy with hit counts and last-hit timestamps from the firewall's own tooling (vendor
  policy optimizer or rule-hit reports; for cloud security groups, flow logs).
- Confirm hit counters have **not been reset** recently (reboots, HA failover and policy pushes can
  reset them on some platforms): you need data covering a full business cycle.

## 2. Classify
| Finding | How to spot | Action |
|---|---|---|
| Zero-hit | no hits over the review period | contact owner, disable, then delete |
| Shadowed | fully covered by an earlier rule (never reachable) | delete or move above the shadowing rule if it was meant to apply |
| Redundant | same effect as another rule further down | merge |
| Over-permissive | `any` service/destination, large subnets, 0.0.0.0/0 from untrusted | tighten using traffic logs (what actually matched) |
| Expired | past its review/expiry tag | recertify or remove |
| Orphaned objects | objects/groups used by no rule | delete |
| No owner / ticket | empty description | find an owner or schedule for removal |
Tools: vendor optimizers, third-party policy analysis tools, or scripts against the exported config.

## 3. Tighten from logs
For an `any` service rule, aggregate traffic logs that hit it over the review period by
destination port/app; replace the rule with the observed set; keep the old rule below, disabled
and logging, for a period.

## 4. Safe removal
1. Change request with the list and evidence.
2. **Disable** (not delete) rules; keep a deny-with-log below if needed to see what would have hit.
3. Wait one business cycle (month end, quarter end jobs).
4. Delete; remove orphaned objects.
5. Record results for audit: counts before/after.

## Verify
- [ ] Review report: total rules, zero-hit, shadowed, over-permissive counts, actions, owners.
- [ ] No incidents traced to removed rules after the wait period.
- [ ] Next review scheduled.

## Checked

2026-10-28: NIST SP 800-41 Rev. 1 (abstract page) supports firewall policy review as a practice but gives no figures. The PCI DSS page returned only a document list, so the six-month review claim, the 90+/90-180 day data windows and the vendor command names (Policy Optimizer, show rule-hit-count, FTD/ASA hitcnt) were removed along with the AlgoSec/Tufin/FireMon names.
Method: documentation only; no commands were run.
