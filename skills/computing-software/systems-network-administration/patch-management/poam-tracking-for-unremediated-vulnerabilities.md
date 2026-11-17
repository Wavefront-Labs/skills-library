---
id: computing-software.systems-network-administration.patch-management.poam-tracking-for-unremediated-vulnerabilities
name: poam-tracking-for-unremediated-vulnerabilities
category: computing-software
field: systems-network-administration
product: patch-management
tags: [poam, plan-of-action-and-milestones, risk-acceptance, deviation-request, fedramp, risk-response, patch-management]
level: practitioner
status: draft
description: "Track vulnerabilities that miss their remediation deadline in a POA&M: required fields, milestones, deviation requests (false positive, operational requirement) and monthly review."
sources:
  - https://csrc.nist.gov/pubs/sp/800/37/r2/final
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# POA&M tracking

**Goal:** every known weakness not fixed within SLA has an owner, a plan and dates, visible to the authorising official.

## What goes in
A POA&M (Plan of Action and Milestones) item for each open finding past its remediation deadline, or any accepted residual risk. FedRAMP-style timelines: high within 30 days, moderate 90, low 180.

## Fields (FedRAMP template)
- POA&M ID, controls affected, weakness name and description, detector source and source identifier (scanner plugin, CVE).
- Asset identifier(s).
- Point of contact, resources required.
- Overall remediation plan, original detection date, scheduled completion date.
- Planned milestones with dates; milestone changes (never overwrite, append).
- Status and status date; vendor dependency flag and vendor check-in date.
- Original and adjusted risk rating; deviation requests.

## Deviation requests
- **False positive**: evidence (package version, config proof, vendor statement) that the finding does not apply.
- **Operational requirement**: the fix would break the mission; compensating controls described; residual risk remains open.
- **Risk adjustment**: downgrade with justification (e.g. not reachable).
Each needs approval and is reviewed periodically.

## Process
1. Export scanner findings older than SLA monthly; create or update items.
2. Owners update milestones; slipped dates get a reason.
3. Close only with evidence (rescan clean).
4. Monthly continuous-monitoring submission or review with the risk owner.

## Gotchas
- POA&M is not a parking lot: items with repeatedly moved milestones need escalation.
- Vendor-dependency items still need mitigations recorded.

## Verify
Every scanner finding past SLA maps to exactly one open POA&M item, and closed items have rescan evidence attached.
