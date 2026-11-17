---
id: computing-software.systems-network-administration.backup-and-recovery.bia-data-collection-and-impact-categories
name: bia-data-collection-and-impact-categories
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [bia-questionnaire, outage-impact, business-impact-analysis, impact-categories, nist-sp-800-34, contingency-planning]
level: practitioner
status: docs-checked
description: "Collect BIA data: interviews, impact categories and rating scales over time, dependencies, peak periods and workarounds feeding MTD, RTO and RPO."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BIA data collection and outage impact categories

**Goal:** collect consistent, comparable impact data from business owners so recovery priorities are evidence-based.

## Before interviews
- List business processes and the systems supporting them (CMDB, architecture diagrams).
- Agree impact categories and the rating scale with leadership so every interview uses the same yardstick. NIST SP 800-34r1 (section 3.2.1) says impact values can be expressed on a scale as an indication of severity if the process could not be performed, and organisations can add categories with units meaningful to them (its example is a "Costs" category in staffing, overtime or fee-related terms).

## Impact categories (an illustrative set, not NIST's list)
| Category | Examples |
|---|---|
| Financial | Lost revenue, penalties, extra costs |
| Operational | Inability to deliver services, backlog growth |
| Legal / regulatory | Missed filings, breach of contract or statute |
| Reputational | Customer loss, media attention |
| Health and safety | Harm to people |
| Data | Loss of records that cannot be recreated |
Choose a rating scale and the time points (for example 1 hour, 1 day, 1 week) that suit your business and rate each category at each point. The guide's own example table pairs processes with potential impacts (operations, reputation, customer service) and maximum tolerable downtime in hours.

## Questionnaire per process
1. Process description, owner, users, volume.
2. Impact ratings over time in each category (where does it become unacceptable? that point informs MTD).
3. Peak periods (month-end, seasonal) when impact is higher.
4. Data loss tolerance: how much recent work could be re-entered (informs RPO)?
5. Dependencies: systems, upstream/downstream processes, suppliers, key people, facilities.
6. Manual workarounds and how long they can be sustained.
7. Minimum resources to run in degraded mode (staff, seats, systems).
8. Backlog recovery time after restoration (the guide notes reprocessing time must be added to the RTO to stay within the MTD).

## NIST SP 800-34 steps
The guide's three BIA steps: (1) determine mission/business processes and recovery criticality; (2) identify resource requirements (facilities, personnel, equipment, software, data files, system components, vital records); (3) identify recovery priorities for system resources. Work with the process owners, leadership and business managers, and include organisations that provide or receive data from the system and the points of contact of interconnected systems.

Definitions from the guide:
- **MTD**: total time the system owner/authorizing official will accept for a process outage, including all impact considerations.
- **RTO**: maximum time a system resource can remain unavailable before unacceptable impact on other resources, the supported processes and the MTD. The RTO must normally be shorter than the MTD.
- **RPO**: the point in time to which data can be recovered given the most recent backup. Unlike RTO it is not part of the MTD; it reflects tolerable data loss.

## Gotchas
- Owners overstate criticality; the agreed scale and leadership review normalise answers.
- Ignoring dependencies produces RTOs that cannot be met (an app RTO of 1 h on a database with a 4 h RTO).

## Verify
Every critical process has completed ratings, dependency lists reconcile with IT's system map, and leadership has signed off the resulting priorities.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (full PDF from nvlpubs.nist.gov, the document behind the csrc.nist.gov page), section 3.2 and Appendix B headings. Targeted reads, not the whole 149 pages. Confirmed: three BIA steps, resource types, MTD/RTO/RPO definitions, RTO shorter than MTD, user-defined impact scales and categories. Removed: the fixed 1-5 scale and the seven specific time points (now presented as choices, not NIST content), the ISO source (not read), and the claim that the guide lists these six categories (it does not; the table is labelled illustrative).

Method: documentation only; no commands were run.
