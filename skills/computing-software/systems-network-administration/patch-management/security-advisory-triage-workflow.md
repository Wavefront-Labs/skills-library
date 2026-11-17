---
id: computing-software.systems-network-administration.patch-management.security-advisory-triage-workflow
name: security-advisory-triage-workflow
category: computing-software
field: systems-network-administration
product: patch-management
tags: [advisory-triage, vulnerability-intelligence, security-advisories, applicability, cisa-kev, epss, patch-management]
level: practitioner
status: docs-checked
description: "Triage incoming vendor security advisories: applicability against inventory, severity and exploitation signals, a patch/mitigate/accept decision and a tracked ticket with SLA."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://www.cisa.gov/stakeholder-specific-vulnerability-categorization-ssvc
  - https://www.first.org/epss/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security advisory triage workflow

**Goal:** turn the daily flood of advisories into a short list of decisions with owners and deadlines.

## Daily loop (one rota owner)
1. **Intake.** Pull new advisories from vendor feeds (MSRC, RHSA/USN/DSA, Cisco PSIRT, VMware/Broadcom VMSA, CSAF feeds), CISA KEV additions, and scanner plugin updates. Deduplicate by CVE.
2. **Applicability.** Query inventory for product and affected versions. Not present: record "not applicable" and stop. Present: note asset count and tiers.
3. **Severity and urgency.** Record CVSS base, vendor severity, KEV status, EPSS probability, exploit availability, and exposure of affected assets. SSVC decision trees (outcomes Track, Track*, Attend, Act; CISA's tree uses Exploitation status, Technical impact, Automatable, Mission prevalence and Public well-being impact) give a repeatable outcome.
4. **Decision.**
   - Act: emergency patch or mitigation now (KEV or active exploitation on exposed assets).
   - Attend: next routine cycle with a tightened SLA.
   - Track: normal cycle.
   - Mitigate: patch unavailable or unsafe; apply vendor workaround and track.
   - Accept: documented risk acceptance with expiry.
5. **Ticket.** One ticket per advisory per owning team, with affected asset list, decision, SLA due date and links.

## Record
Keep a triage log: advisory ID, date received, decision, decider, ticket. It proves timeliness to auditors and feeds metrics (time from release to decision).

## Gotchas
- Vendor "Important" can still be KEV-listed; exploitation evidence beats labels.
- Backported Linux fixes keep old version strings; check the advisory's fixed package release, not upstream version.

## Verify
Every advisory in the period has a logged decision within the triage SLA (for example one business day; set your own).

## Checked
Date: 2026-10-27. Documentation: CISA SSVC page (decision points, outcome names), FIRST EPSS page, NIST SP 800-40 Rev. 4 page. The rest of the skill is process guidance with no vendor-specific figures; SLA values are labelled as local policy.
Method: documentation only; no commands were run.
