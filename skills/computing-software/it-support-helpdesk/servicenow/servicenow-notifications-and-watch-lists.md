---
id: computing-software.it-support-helpdesk.servicenow.servicenow-notifications-and-watch-lists
name: servicenow-notifications-and-watch-lists
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, servicenow-notifications, watch-list, work-notes-list, email-notifications, sys-email, notification-troubleshooting]
level: practitioner
status: gated
description: "ServiceNow email notifications and watch lists: when/who/what conditions, watch list vs work notes list, why an email did not send, and checking sys_email logs."
sources:
  - "https://www.servicenow.com/docs/bundle/xanadu-platform-administration/page/administer/notification/concept/c_EmailNotifications.html"
  - "https://www.servicenow.com/docs/bundle/xanadu-platform-administration/page/administer/notification/task/t_TroubleshootEmailNotifications.html"
  - "https://www.servicenow.com/docs/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# servicenow-notifications-and-watch-lists

A notification (System Notification > Email > Notifications) has **When to send**
(insert/update/event + conditions), **Who will receive** (users, groups, fields such as
caller, assigned_to, watch_list), and **What it will contain** (template, subject, body).

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Watch list vs work notes list
| Field | Gets | Use for |
|---|---|---|
| Watch list | Customer-visible updates (additional comments) | Manager, delegate, a colleague with the same fault |
| Work notes list | Internal work notes | Other IT staff following the ticket |

Never put an end user on the work notes list; they would receive internal notes.

## Why didn't the email go?
1. **System Logs > Emails** (`sys_email`): is there a record? Type `send-ready`, `sent`,
   `send-ignored` or failed. No record means the notification never triggered.
2. Open the record: the **Notification** field and recipients; "Ignored" reasons
   (recipient inactive, no email, user notification preference off).
3. Check notification **conditions** and "Send to event creator" (off by default: the
   person who made the update does not get the email).
4. User's own notification preferences (profile > Notification preferences) can disable
   a notification category.
5. Email sending on instance: `glide.email.smtp.active` and email properties; sub-prod
   instances often have sending disabled or redirected to a test address.
6. Weight: when several notifications on the same table/event fire, only the highest
   weight is sent per recipient.

## Good practice
- Fewer, clearer notifications: assigned to you, assigned to your group (unassigned),
  comment added, resolved, SLA warning.
- Put the ticket number and short description in the subject; the reply-to watermark
  (`Ref:MSG...`) lets replies append to the right record.
- Major incidents: send updates via a dedicated notification or communication plan rather
  than adding hundreds of watchers.

## Gotchas
- Watch list entries can be emails of non-users; replies from them may create new
  records if inbound email actions don't recognise the sender.
- Bulk updates (list edits, imports) can fire thousands of notifications; check before.
- Out-of-office replies can loop with update notifications; inbound actions should ignore
  auto-replies.

## Verify
Trigger the notification on a test record, find the `sys_email` entry, confirm
recipients and that watch-list users got comments but not work notes.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
