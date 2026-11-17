---
id: computing-software.it-support-helpdesk.servicenow.work-notes-vs-additional-comments
name: work-notes-vs-additional-comments
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, work-notes-vs-comments, work-notes, additional-comments, customer-updates, incident-management, journal-fields]
level: practitioner
status: gated
description: "Use ServiceNow work notes vs additional comments correctly: who sees what, notification triggers, update cadence, and recovering from a note posted to the wrong field."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/incident-management/concept/c_IncidentManagement.html"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-user-interface/page/use/using-forms/concept/c_JournalFields.html"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-administration/page/administer/notification/concept/c_EmailNotifications.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# work-notes-vs-additional-comments

ServiceNow tasks have two journal fields. Mixing them up is the most common way an
agent leaks internal detail to a caller, or leaves the caller in silence.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

| Field | Column | Visible to | Default notification |
|---|---|---|---|
| Additional comments (Customer visible) | `comments` | Caller, watch list, portal | "Incident commented" to caller + watch list |
| Work notes | `work_notes` | Fulfillers (itil role) only | "Incident work noted" to assigned to + work notes list |

In Agent Workspace the compose box has a toggle; the compose border colour shows which
field is active. Check it before every post.

## What goes where
- **Comments**: what you did in plain language, what you need from the user, the next
  update time. Write as if the user forwards it to their manager.
- **Work notes**: commands run, log excerpts, hostnames, vendor case numbers, routing
  discussion, anything with other people's PII or security detail (IOCs, accounts under
  investigation).
- Never put passwords, LAPS/BitLocker keys or MFA codes in either field. Journal entries
  live in `sys_journal_field` and agents cannot edit them.

## Update cadence (typical; align to your SLA)
- P1: customer-visible update every 30 min even if nothing changed; P2 every 2 h; P3/P4 on
  each state change or at least every 3 business days.
- Moving to On Hold (Awaiting Caller) without a comment saying *what* you wait for drives
  reopens and poor CSAT.

## Posted to the wrong field
1. Agents can't delete comments. An admin can delete the `sys_journal_field` row plus the
   matching `sys_audit` / `sys_history_line` rows, but the email may already have gone:
   check `sys_email` for the record and timestamp.
2. If the email went: tell your team lead, follow the data-incident procedure if the note
   held personal or security data, and send a short correction.
3. Prevent repeats: an onSubmit client script that warns when `comments` contains UNC
   paths, IP addresses or "password"; or personalise the form so work notes show first.

## Lists and reports
- No customer-visible update for 3 days: `sys_updated_on` is not the last comment. Report
  on `sys_journal_field` with `element=comments` grouped by `element_id`, or use a "last
  customer update" field if your instance has one.
- `watch_list` receives comments; `work_notes_list` receives work notes. Adding a manager
  to the wrong list is a frequent complaint.

## Gotchas
- Caller email replies land in `comments` via the inbound email action; an agent replying
  to the notification email also lands in comments (customer visible).
- Some instances copy work notes from child to parent (or vice versa) by business rule;
  check before writing sensitive notes on a child of a major incident.

## Verify
Impersonate the caller (or view in the portal) and confirm only the intended comments
are visible, and the email log shows the expected notification.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
