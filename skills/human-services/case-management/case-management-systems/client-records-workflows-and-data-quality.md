---
id: human-services.case-management.case-management-systems.client-records-workflows-and-data-quality
name: client-records-workflows-and-data-quality
category: human-services
field: case-management
product: case-management-systems
tags: [case-management, case-management-system, cms, client-management-system, crm, salesforce, salesforce-nonprofit, dynamics-365, penelope, apricot, casebook, ndis, welfare-platform, client-records, duplicate-records, data-quality, workflow-queues, tasks, reporting, funder-reporting, privacy, access-control, caseworker]
level: practitioner
status: draft
description: "Work well in any client/case-management system: find-before-create to avoid duplicates, structured fields over free text, task queues as your safety net, and clean data for funder reports."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Client records, workflows and data quality in case-management systems

**Goal:** use the system so that it remembers for you, shows the true state of every case,
and produces reports nobody has to fix by hand.

This is product-class guidance: it applies broadly to CRM-style case systems (e.g. Salesforce
nonprofit builds, Dynamics-based systems, Penelope, Apricot and many in-house or government
platforms). Menu names and features differ — **unconfirmed for any specific product**;
use your system's own training and admin guidance.

## 1. Find before you create
Duplicate client records are the most common and damaging data error: history splits,
risk flags are missed, reports double-count.
1. Search by surname, date of birth and a partial first name (spelling varies: "Mohammed",
   "Muhammad"; "Katie", "Catherine").
2. Try previous names and alternative IDs if the system holds them.
3. Only create new if nothing matches; if you find a duplicate later, **request a merge**
   through the admin process, don't just stop using one.

## 2. Structured fields over free text
Reports, alerts and funder data come from structured fields (dropdowns, dates, checkboxes),
not from notes. If you write "client now housed" in a note but leave the housing-status field
unchanged, the system — and your manager's dashboard — still thinks they're homeless.
Rule: **every significant change gets both a note and a field update.**

Typical fields to keep current: address/housing status, contact details and safe-contact
flags, consent records, risk/alert flags, case status, assigned worker, plan goals and review
dates, referral statuses, outcome scores.

## 3. Let workflows carry the memory
- Create a **task with a due date** for every follow-up you promise (referral check, review,
  document chase). Your task queue becomes the caseload safety net.
- Clear or reassign tasks; a queue full of stale tasks is ignored.
- Use built-in review-date reminders rather than your own calendar.

## 4. Alerts and sensitive information
- Use risk/alert flags for things the next person *must* know (violence risk to workers,
  safe-contact only, protection orders). Keep them current — stale alerts get ignored.
- Restricted/sensitive records (family-violence addresses, HIV status, witness protection):
  use the system's access restrictions; never put such details in widely visible fields.
- Only open records you have a work reason to view — access is usually audited.

## 5. Reports and data quality
- Learn the handful of reports you need: your caseload list, overdue reviews, open referrals,
  outcomes.
- Run a monthly self-check: cases with no activity, missing mandatory fields, closed cases
  with open tasks.
- Funder reports are only as good as field entry; if counts look wrong, check the definitions
  (e.g. what counts as "open" or "a contact") before blaming the system.

## Gotchas
- Logging contacts days later with today's date distorts activity reports; back-date to the
  actual contact date where the system allows.
- Free-text "N/A" or "unknown" in a date or ID field breaks matching and reports.
- Shared logins break audit trails — never share credentials.
- Offline/mobile entry may sync later; check it actually synced.
- Exporting client data to personal spreadsheets is usually a privacy breach.

## Verify
- [ ] Searched with name variants and DOB before creating any new client.
- [ ] Field values match the latest note (housing, status, risk, consent).
- [ ] Every promised follow-up exists as a dated task.
- [ ] Alert flags current; sensitive info only in restricted fields.
- [ ] Monthly data-quality self-check done with no unresolved gaps.
