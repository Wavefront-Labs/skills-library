---
id: computing-software.systems-network-administration.patch-management.stakeholder-communication-during-zero-days
name: stakeholder-communication-during-zero-days
category: computing-software
field: systems-network-administration
product: patch-management
tags: [incident-communication, stakeholder-communication, zero-day, emergency-patching, patch-management]
level: practitioner
status: draft
description: "Communicate during a zero-day patch response: audiences, cadence, templates for initial alert, status updates and closure, and avoiding mixed messages or leaked details."
sources:
  - https://csrc.nist.gov/pubs/sp/800/61/r3/final
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
  - https://sre.google/sre-book/managing-incidents/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stakeholder communication during zero-days

## Audiences and what they need
| Audience | Needs |
|---|---|
| Executives / CISO | exposure in plain words, business impact, ETA, decisions needed |
| App/system owners | which of their systems, what downtime, what they must test |
| Service desk | user-facing symptoms, script for callers, outage times |
| All staff (sometimes) | action required (restart, update browser), phishing warning |
| Customers/regulators | only via legal/comms; facts, no speculation |

## Cadence
- Initial note within 1-2 hours of declaring.
- Status updates on a fixed schedule (e.g. every 4 h during active response, daily after), even if "no change".
- Closure note with summary and follow-ups.
One comms owner; others do not send their own versions.

## Templates
Initial:
```text
Subject: [Emergency patch] CVE-YYYY-NNNN in <product> - action in progress
What: Actively exploited flaw in <product>. Exposure: <N> systems, <M> internet-facing.
Doing: Mitigation applied to internet-facing at HH:MM; patching starts HH:MM.
Impact: <service> restarts between HH:MM and HH:MM.
You need to: <owners test X by Y> / nothing.
Next update: HH:MM. Contact: <bridge/channel>.
```
Update: progress numbers (patched/total), blockers, changes to impact, next update time.
Closure: final numbers, exceptions remaining with owners, whether compromise was found, PIR date.

## Gotchas
- Do not include exploit details or unpatched host lists in broad email; use need-to-know channels.
- Avoid "we are not affected" before the asset search is complete; say "assessment in progress".
- Keep timestamps in one timezone and say which.

## Verify
Every update sent on time, numbers in comms match the remediation tracker, and the PIR reviews communication timeliness.
