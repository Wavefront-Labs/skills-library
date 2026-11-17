---
id: law-government.judiciary-and-courts-administration.court-case-management-systems.docketing-e-filing-review-and-records-workflows
name: docketing-e-filing-review-and-records-workflows
category: law-government
field: judiciary-and-courts-administration
product: court-case-management-systems
tags: [judiciary-and-courts-administration, court-case-management-systems, cms, case-management-system, odyssey, tyler-technologies, enterprise-justice, cm-ecf, nextgen-cm-ecf, pacer, e-filing, efm, efsp, docketing, docket-entry, event-codes, clerk-review, filing-rejection, scheduling, calendaring, hearings, sealed-documents, redaction, public-access, records-retention, data-quality, statistical-reporting, notices-of-electronic-filing]
level: practitioner
status: draft
description: "Operate court case-management and e-filing systems such as Odyssey and CM/ECF: clerk review of filings, accurate docket events, scheduling, sealed records, and data quality for reporting."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Docketing, e-filing review and records workflows

**Goal:** a docket that is accurate, timely and trustworthy — because orders, deadlines,
public access and statistics all flow from it. Covers court-side use of systems such as
Tyler Technologies' Odyssey (now marketed within its Enterprise Justice suite) and the
US federal judiciary's CM/ECF (with PACER public access). Screens, event codes and
configuration are court-specific; consult your court's procedures manual — this skill
describes the workflow, not exact menus.

## 1. Understand the data model
- **Case** → **parties** (with roles) → **events/docket entries** → **documents**,
  **hearings**, **judgments/dispositions**, **financials** (fees, fines).
- **Event codes** drive everything downstream: deadlines, notices, statistics, public
  display. Choosing "Motion to Dismiss" vs generic "Motion" can decide whether a response
  deadline is calculated or a judge's motion report shows it. Learn your court's code
  list and use the most specific correct code.
- Case-status codes (open, stayed, closed, reopened) feed time-to-disposition reports —
  update them at every status-changing event.

## 2. E-filing review (clerk queue)
In many state systems filings arrive through an e-filing manager from service
providers and sit in a **review queue**; in CM/ECF, attorneys docket their own entries
and the clerk performs **quality control** afterwards.
For each filing check:
1. Correct case and party; correct filer role.
2. Document matches the selected event (a motion filed as "Notice" breaks deadlines).
3. Fees paid or waiver on file.
4. Required components: signatures, certificate of service, proposed order where
   required, page limits/formatting per local rules.
5. **Privacy**: personal identifiers redacted per rules (e.g. partial account numbers,
   minors' initials); sealed/confidential documents filed under the correct security level.
Reject/return only for reasons the rules allow, with a clear reason code and message;
otherwise accept and correct docket text where policy permits (note "modified by clerk").
Accepted filing time stamps matter for deadlines — know the rule for when a filing is
deemed filed.

## 3. Docketing judicial actions
- Enter orders the same day signed; link them to the motion they resolve (so the motion
  drops off pending reports).
- Docket text should be complete and searchable: what was ordered, deadlines, hearing dates.
- Generate and verify **notices** (notices of electronic filing / service to parties);
  paper service for parties not registered.
- Judgments: correct parties, amounts, interest, and disposition codes.

## 4. Scheduling
- Use the calendar module tied to the judge's availability and courtroom resources;
  avoid manual calendars outside the system.
- Set hearing types consistently (status, motion, trial) so trial-date-certainty and
  continuance data are measurable.
- When continuing a hearing, record who requested it and the reason code.

## 5. Records, access and retention
- Security levels: public, confidential, sealed, judge-only. Verify after every sealing
  order that the documents *and* docket text are restricted as ordered.
- Public portals/terminals: confirm what case types are excluded (e.g. juvenile, mental
  health, adoption) by law.
- Records retention schedules: purge or archive per schedule with documented approvals.
- Certified copies issued only from the official record.

## 6. Data quality and reporting
- Run exception reports: cases with no activity beyond X days, pending motions past
  due, open cases with disposition events, duplicate parties.
- Fix at the source and train on recurring errors; statistics reported to state/federal
  bodies depend on clean codes.

## Gotchas
- Generic event codes chosen for speed — silently break deadline calculations and statistics.
- Sealed documents leaking via unrestricted docket text or attachments.
- Duplicate party records splitting a person's case history.
- Upgrades change workflows; re-test custom reports after each release.

## Verify
- [ ] Each filing reviewed for case, party, event code, fees, privacy and security level.
- [ ] Orders docketed same day and linked to the motions they resolve.
- [ ] Hearings and continuances recorded with type and reason codes.
- [ ] Sealed items and their docket text confirmed restricted.
- [ ] Exception reports run on a schedule and errors corrected.
