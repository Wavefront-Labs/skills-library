---
id: computing-software.networking-hardware-and-wireless.check-point.rulebase-hit-count-and-cleanup
name: rulebase-hit-count-and-cleanup
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, hit-count, unused-rules, rulebase-cleanup]
level: practitioner
status: draft
description: "Use Check Point hit counts and rule-base tools to find unused rules, shadowing and expiry, and clean up safely."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_LoggingAndMonitoring_AdminGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rulebase hit count, cleanup and rule review

- Enable **Hit Count** in the policy (Manage & Settings > Blades > Advanced > Hit Count, or per layer). It counts matches per rule across all gateways; columns show hits, percentage, level (Zero/Low/Medium/High/Very High) and "last hit" date.
- A rule with zero hits for a retention period (commonly 90 days) is a deletion candidate; check **Last Hit** and the keep-for period, not just the count, because the counter resets if you disable and re-enable.
- Rule expiry: a rule's **Time** column can use a time object (scheduled start/end), but there is no automatic deletion, so delete it manually.
- Command line:
```
mgmt_cli -r true show access-rulebase name "Network" details-level full show-hits true hits-settings.from-date "2025-01-01" hits-settings.to-date "2025-06-30" --format json
mgmt_cli -r true set access-rule layer "Network" uid "<uid>" enabled false
```
- Approach: disable first (not delete), add a comment with the date and ticket, install, watch for complaints for a cycle, then delete. Keep the disabled rule visible by number.
- SmartConsole also warns on **Shadowed rules** only via the Policy "Verify" for some cases; use the management "Rule base audit" or SmartConsole **Policy Verification** (Install Policy checks anti-spoofing and some conflicts).
- Gotcha: Hit counts are per gateway installation; after a policy move to a new gateway name the history is lost. Management HA syncs counts but not instantly.

Verify: show the hit count of a rule you know is used (e.g. DNS) as non-zero; after change confirm the "Last Hit" updates within minutes.
