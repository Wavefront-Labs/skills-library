---
id: computing-software.it-support-helpdesk.servicenow.servicenow-lists-navigation-and-email-client
name: servicenow-lists-navigation-and-email-client
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, list-personalization, servicenow-navigation, servicenow-email-client, list-editing, keyboard-shortcuts, favorites]
level: practitioner
status: gated
description: "Work faster in ServiceNow: navigator and favourites, keyboard shortcuts, list personalisation and inline editing, saved filters, and sending email from a record."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-platform-user-interface/page/use/navigation/concept/c_NavigationAndTheUserInterface.html"
  - "https://www.servicenow.com/docs/bundle/zurich-platform-user-interface/page/use/using-lists/concept/c_UsingLists.html"
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/administer/notification/concept/c_EmailClient.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# servicenow-lists-navigation-and-email-client

## Navigation
- **Filter navigator** (All menu): type a module name, or a table followed by `.list`
  (e.g. `incident.list`) or `.form` to open a new record. `.LIST` / `.FORM` open in a new
  tab.
- **Favourites**: star modules or drag a list breadcrumb to favourites to save a filtered
  list ("My group's unassigned P2s"). Rename and colour them.
- **History** shows recently viewed records.
- Global search for ticket numbers jumps straight to the record.
- Keyboard: Next Experience lists its shortcuts in the user menu (Keyboard shortcuts);
  learn the ones for global search, the navigator and saving a form, and check them on
  your release since they differ between UI16 and Next Experience.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## List personalisation
- Gear icon on the list: choose and order columns, wrap text, compact rows. This is per
  user and doesn't affect others.
- Filters: build with the condition builder, then **Save filter** (for you or a group).
- Group by (right-click a column header) to see counts by assignee or state.
- **List editing**: double-click a cell to edit inline (if the list control allows);
  select several rows and edit one cell to update them all. Check business rules and
  mandatory fields still apply; inline edits skip some client scripts.
- Right-click column > Show matching / Filter out for quick filtering.

## Email client from records
- Form context menu > **Email** (when the email client is enabled for the table) opens a
  composer with the record's caller and watch list, a template picker and quick messages.
- Emails sent this way are logged on the record (Activity) and replies thread back by
  the watermark.
- Use for one-off messages to someone not on the ticket (a vendor); routine updates
  belong in additional comments, which notify the caller.

## Verify
Your common queues are one click away in favourites, lists show the columns you triage
by, and emails sent from records appear in the activity stream.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
