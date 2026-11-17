---
id: computing-software.it-support-helpdesk.servicenow.zendesk-macros
name: zendesk-macros
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, zendesk, zendesk-macros, canned-responses, saved-replies, placeholders, macro-library, consistent-replies]
level: practitioner
status: docs-checked
description: "Build and maintain a Zendesk macro library: applying, previewing and troubleshooting macros, placeholders, keyboard shortcut and bulk use."
sources:
  - "https://support.zendesk.com/hc/en-us/articles/4408887656602-Creating-macros-for-tickets"
  - "https://support.zendesk.com/hc/en-us/articles/4408886858138-Zendesk-Support-placeholders-reference"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zendesk-macros

A macro is a prepared response or action that an agent applies manually when creating or updating tickets: a comment plus field changes. It suits requests that can be answered with a single, standard response or action. Macros cannot be set up for specific channels.

## Starting macros Zendesk provides
"Close and redirect to topics", "Requester not responding" (reminder on a pending ticket), "Downgrade and inform" (priority to low) and "Take it!" (assign to yourself). They can be used as is, edited or cloned.

## Applying macros
- Menu: in a ticket click Apply macro in the bottom toolbar, filter by typing the start of the name, select. Your most-used macros of the past week (typically five) appear at the top unless that display is disabled.
- Keyboard: with Agent Workspace, type a slash (/) in the comment (typically seven most used shown). Shortcuts are on by default.
- If the macro changes the comment you can edit the text before submitting. Set an insertion point first to control where the text lands.
- Several macros can be applied to one ticket (for example two answers for two questions), but what one macro does can be undone by another. Applied macros show in the ticket's events log.
- Macros can be applied to several tickets from views (bulk update).
- Preview: the Open preview icon (or Shift + Enter on the tooltip) shows the title, description and the fields, comments (including placeholders and dynamic content) and attachments it will change.

## Example (illustrative)
```text
Name:    Password reset done
Actions: Comment (public):
           Hi {{ticket.requester.first_name}},
           I've reset your password. Sign in with the temporary password you were sent;
           you'll be asked to set a new one. Reply to this email if it doesn't work.
         Status: Pending
```
Placeholders such as `{{ticket.requester.first_name}}` come from the placeholder reference. Setting the status in the macro keeps the reply and the state change together.

## When a macro does not apply as expected
- A ticket field the macro updates must appear on the ticket form.
- If the ticket was updated at the same time from another source, wait for the latest changes and try again.
- If you lack permission for a change the macro makes, that action will not occur.
- A manual revert or a contradicting second macro can make the first look unapplied.
- Triggers or automations can conflict with the update and cause tag collisions; check the events log.
- If the ticket tab is closed before submitting, the comment text is kept but the macro is not shown in the events log.

## Problem and incident tickets
Use caution with placeholders when applying macros to problem and incident tickets; the values may populate wrongly. Escape the placeholder with a backslash, for example `\{{ticket.requester.first_name}}`, so it populates the related incident ticket's value.

## Verify
Apply the macro to a test ticket, preview it first, then check the rendered comment and the fields it changed in the events log.

## Checked

Confirmed against the Zendesk article on applying macros and the placeholder reference: starter macros, menu and slash shortcut use, multiple macros, preview, troubleshooting list, problem and incident placeholder escaping. Removed the :: folder naming, tag-per-macro reporting, usage-based pruning, library structure and writing-rule guidance, and the usage-report article source (404), since the readable pages do not state them.

Method: docs-only read of cited pages, 2026-11-08
