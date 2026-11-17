---
id: computing-software.it-support-helpdesk.servicenow.zendesk-triggers-and-automations
name: zendesk-triggers-and-automations
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, zendesk, zendesk-triggers, zendesk-automations, business-rules, ticket-routing, auto-solve, placeholders, liquid]
level: practitioner
status: docs-checked
description: "Zendesk business rules: event-based triggers vs hourly time-based automations, their limits, nullifying conditions, 96-hour close, and placeholders."
sources:
  - "https://support.zendesk.com/hc/en-us/articles/4408822236058-About-triggers-and-how-they-work"
  - "https://support.zendesk.com/hc/en-us/articles/4408832701850-About-automations-and-how-they-work"
  - "https://support.zendesk.com/hc/en-us/articles/4408886858138-Zendesk-Support-placeholders-reference"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zendesk-triggers-and-automations

| | Triggers | Automations |
|---|---|---|
| Fires on | Immediately after a record (such as a ticket) is created or updated | Time events: all automations run once an hour on non-closed tickets |
| Typical use | Routing, notifications, tagging | Reminders, escalations, closing solved tickets |
| Built from | Conditions ("if") and actions ("then") | Conditions and actions, with a time condition |
| Must | Account for interplay with other triggers and automations | Include a nullifying action or a condition that can be true only once |

## How triggers work
- Ticket triggers run any time a ticket is created or updated; a "Ticket channel is {channel}" condition lets them cover chat, messaging and calls too. Object triggers do the same for custom object records. Chat and messaging triggers run on a single admin-chosen event.
- Conditions come as "all" (every one must be true) and "any" (one or more must be true); ticket and object triggers can combine them.
- Ticket triggers do not fire on closed tickets, but can fire as a ticket is being set to closed (not when the system auto-closes after 28 days).
- Actions of one ticket trigger can affect how other triggers fire on the same ticket, and changes made by automations can cause triggers to run (and the reverse). Design them together.
- Triggers, like all business rules, must be smaller than 65 KB. Manage them in Admin Center > Objects and rules > Business rules > Triggers.

## Core triggers for an IT desk (illustrative)
1. Route by form or category: ticket is created AND form is "Access request" -> set group.
2. Tag VIPs: requester organisation condition -> add a tag, raise priority.
3. Notify the requester on receipt, public comment and solve (edit the standard wording).
4. Notify the group on assignment.

## How automations work
- Automations are time-based, run every hour (not necessarily at the top of the hour) and never on closed tickets.
- Each automation can fire on at most 1,000 tickets per hour; the rest are handled in later hours.
- Each ticket can be updated at most 100 times by automations; the Close ticket automation is the exception. Tickets past 100 automation audits are excluded from the hourly run.
- Active automations must be unique, at most 500 can be active, and each must be smaller than 65 KB.
- Automations do not run on accounts nobody has signed in to for 14 days.
- Automations run in order and update the ticket as they fire, so one automation's action can satisfy the next one in the same hour.

## Use automations only once per ticket
Every hour the conditions are re-checked, so an automation needs either an action that nullifies one of its conditions or a condition that can be true only once. Without it, it fires every hour on the same ticket.
- Nullify a priority condition by changing the priority in the action.
- A "hours since created is 4" style condition is true only once, but because run times vary within the hour an "is" condition can, rarely, never evaluate true (more likely on large accounts).
- An easy nullifier is a tag: the automation requires the tag to be absent and adds it when it fires.
- Standard example: the Close ticket automation closes tickets 96 hours (4 days) after they were solved; "status is Solved" is nullified by the action "status is Closed".
- Time precision: the first run after an event counts as zero hours since it, so "two hours after solved" fires on the third run when the ticket is solved at 9:15 and runs happen at 10:10, 11:10 and 12:10.

## Placeholders
`{{ticket.id}}` (as `#{{ticket.id}}` it becomes a clickable link), `{{ticket.title}}`, `{{ticket.requester.first_name}}`, `{{ticket.latest_public_comment}}` and `{{ticket.url}}` are listed in the placeholder reference. `{{ticket.url}}` omits "http://" and uses the agent URL in macros, ticket comments and side conversations. Placeholders can also be used with Liquid markup, as the reference shows for organisation and CC data.

## Verify
Open the ticket's events (audit trail): it shows when an automation fired on that ticket, which helps prove order and find the rule behind an unexpected change.

## Checked

Confirmed against the Zendesk articles on triggers, automations and the placeholder reference: trigger run timing, closed-ticket behaviour, 65 KB size limit, hourly automation runs, 1,000 tickets per hour, 100 automation updates per ticket, 500 active automations, 14-day inactivity rule, nullifying conditions, the 96-hour Close ticket automation and the listed placeholders. Removed the trigger-ordering and restart claims, the claim that Zendesk rejects automations without a nullifier, the 28-day window, the deactivate-versus-delete audit claim, the internal-note trigger gotcha, the SLA-breach automation condition, the Liquid if example and the specific condition names, none of which the cited pages state.

Method: docs-only read of cited pages, 2026-11-08
