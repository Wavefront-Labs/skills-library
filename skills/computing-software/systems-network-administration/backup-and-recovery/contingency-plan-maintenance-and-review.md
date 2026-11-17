---
id: computing-software.systems-network-administration.backup-and-recovery.contingency-plan-maintenance-and-review
name: contingency-plan-maintenance-and-review
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [plan-maintenance, contingency-plan, plan-review, record-of-changes, nist-sp-800-34, business-continuity]
level: practitioner
status: docs-checked
description: "Keep contingency and DR plans current: review cycles, change triggers, contact list upkeep, version control, record of changes and distribution."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contingency plan maintenance and review

**Goal:** the plan in the binder matches the systems and people of today.

## Review cycle
- NIST SP 800-34 Rev. 1 (section 3.6) says the plan should be reviewed regularly as part of change management, at an organization-defined frequency or whenever significant changes occur to any element of the plan.
- Certain elements, such as contact lists, need more frequent reviews, and plans for moderate- or high-impact systems should be reviewed more often. Set the actual frequencies in your own policy.
- Minimum review focus per NIST: operational requirements, security requirements, technical procedures, hardware/software/equipment, names and contact details of team members and of vendors (including alternate and offsite vendor contacts), alternate and offsite facility requirements, and vital records.
- The ISCP Coordinator also evaluates supporting information: alternate site contract (including testing times), offsite storage contract, software licences, MOUs or vendor SLAs, interconnection agreements, recovery strategy, training materials and testing scope.

## Triggers for an unscheduled update
- Significant change to any element of the plan (systems, procedures, organisation, vendors).
- A significant change means the BIA should be updated too, to find new contingency requirements or priorities (changed RTO/RPO).
- Lessons learned: NIST asks for an after-action report with lessons learned after recovery events, to be used to update the plan.
Hook this into change management: changes affecting recoverability include a "DR plan updated?" checkbox.

## Version control
- The ISCP Coordinator coordinates changes and keeps a **record of changes**; NIST's sample table lists page number, change comment, date of change and signature.
- Strict version control: old plans or pages are returned to the Coordinator in exchange for the new ones.
- The Coordinator keeps a record of copies of the plan and to whom they were distributed.

## Storage and distribution
- The plan contains sensitive operational and personnel information, so mark and control its distribution.
- Per NIST, copies go to recovery personnel, and a copy is stored at the alternate site and with the backup media, so the plan is available when local copies cannot be accessed.
- Store with the plan: vendor contracts (SLAs), software licences, system user manuals, security manuals and operating procedures.

## Gotchas
- Plans updated only at audit time drift; tie updates to change management.
- Hyperlinks to wikis that will be down during a disaster are not a plan.

## Verify
A random sample of contacts, procedures and system names from the plan is accurate when checked against current reality.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (full PDF from nvlpubs.nist.gov, the document behind the csrc.nist.gov page), section 3.6 Plan Maintenance and section 4.4 (after-action report). Targeted reads of those sections, not the whole 149 pages. Confirmed: organisation-defined review frequency, more frequent for contact lists and moderate/high plans, review elements, record of changes columns, strict version control, copies at alternate site and with backup media, BIA update on significant change. Removed: the "at least annually" and "quarterly" figures presented as NIST recommendations (the guide leaves frequency to the organisation for plan review), the ISO source (not read), "approvals recorded for each version" (not in the guide), and the version/date/author table layout (replaced by the guide's columns).

Method: documentation only; no commands were run.
