---
id: computing-software.systems-network-administration.backup-and-recovery.bia-report-and-sign-off
name: bia-report-and-sign-off
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [bia-report, business-impact-analysis, bia, nist-800-34, sign-off, recovery-priorities]
level: practitioner
status: docs-checked
description: "Assemble the BIA report from interviews and impact data: MTD, RTO, RPO, recovery priorities, gaps and formal sign-off by business owners."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BIA report and sign-off

**Goal:** one approved document the contingency plan, backup design and DR budget all cite.

## Report structure (follows the SP 800-34 Rev. 1 Appendix B template)
1. **Overview** - system name and acronym, completion date, purpose (the three BIA steps). The BIA is built into the ISCP and may support the DRP and cyber incident response plan.
2. **System description** - architecture and functionality, operating environment, physical location, users, external partners, backup procedures, with an architecture diagram. The template says this can come from the System Security Plan.
3. **BIA data collection** - the template allows interviews, workshops, email, questionnaires or any combination; record which you used.
4. **Process and system criticality** - mission/business processes that depend on the system, outage impacts by impact category (with severity values defined for the organisation), and estimated downtime.
5. **MTD, RTO, RPO table** per process, in hourly increments (the sample row is 72, 48 and 12 hours), with a description of the drivers (mandate, workload, performance measure) and any alternate means or manual workaround, or a statement that none exist.
6. **Resource requirements** - table of system resources/components with platform/OS/version and description.
7. **Recovery priorities** - ordered list of resources with the recovery time expected after a worst-case disruption (complete rebuild, repair or replacement), plus alternate strategies in place such as spare equipment and vendor support contracts.

Beyond the template (practice, adapt to your governance): a gaps section comparing current capability with targets, and a sign-off page for the business owner(s), system owner and authorising official.

## Practical rules
- Show impact as a timeline table; executives sign faster when they see where "tolerable" turns "severe".
- Check that the RTO is shorter than the MTD by at least the reprocessing time, as the guide says (section 3.2.1); if not, the RTO is wrong.
- Every gap gets an owner, an estimated cost to close, and a decision (fund, accept risk, transfer).
- Version it, date it, and set review triggers. The guide says to update the BIA when a significant change occurs (section 3.6).

## Gotchas
- A BIA that IT signs alone is not a BIA. Get the business owner signature; they own the downtime.
- Avoid single "criticality" scores with no time dimension; they cannot drive RTO.
- Keep a copy outside the systems it describes (see plan distribution).

## Verify
The signed report is stored somewhere controlled, and RTO/RPO values copied into the ISCP and backup policy match exactly.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (full PDF from nvlpubs.nist.gov, the document behind the csrc.nist.gov page), Appendix B template and sections 3.2 and 3.6. Targeted reads, not the whole 149 pages. Confirmed: template sections, hourly-increment MTD/RTO/RPO table, drivers and workaround notes, recovery priorities with worst-case RTO, BIA update on significant change. Removed: the ready.gov source (not read), the template attribution of the nine-item layout, the fixed impact categories and time buckets, the example gap figures, "annual" review, the GRC-tool storage detail. Gaps and sign-off sections are labelled as practice beyond the template.

Method: documentation only; no commands were run.
