---
id: computing-software.it-support-helpdesk.device-provisioning.leaver-mailbox-and-onedrive-retention
name: leaver-mailbox-and-onedrive-retention
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, leaver-data-retention, offboarding, shared-mailbox, inactive-mailbox, onedrive, litigation-hold, leaver-mailbox-delegation, license-reclamation]
level: practitioner
status: draft
description: "Keep a leaver's mail and files available without wasting licences: convert to shared, inactive mailboxes via holds, OneDrive manager access and retention, before deleting the user"
sources:
  - "https://learn.microsoft.com/en-us/microsoft-365/admin/email/convert-user-mailbox-to-shared-mailbox"
  - "https://learn.microsoft.com/en-us/purview/inactive-mailboxes-in-office-365"
  - "https://learn.microsoft.com/en-us/sharepoint/retention-and-deletion"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# leaver-mailbox-and-onedrive-retention

## Decide with the manager and records policy
What must be kept, for how long, and who needs access: continue receiving mail (shared
mailbox), legal/regulatory retention (hold), or just a file handover.

## Mailbox options
| Need | Do |
|---|---|
| Colleagues keep working the mailbox | `Set-Mailbox -Identity jsmith -Type Shared`, then grant FullAccess/SendAs to the manager; remove the licence afterwards (shared mailboxes under 50 GB without archive/hold do not need one) |
| Keep for compliance, nobody works it | Apply a retention policy or litigation hold **before** deleting the user, so the mailbox becomes **inactive** and is kept with no licence |
| Auto-reply to senders | `Set-MailboxAutoReplyConfiguration -Identity jsmith -AutoReplyState Enabled -ExternalMessage "..."` |
| Forward mail | Prefer shared mailbox access over forwarding; forwarding outside the org is often blocked |

## OneDrive
- When the user is deleted, OneDrive is kept for the retention period (default 30 days,
  configurable in SharePoint admin center > Settings > OneDrive retention) and the manager
  gets access by email.
- Better: before deleting, move business files to the team's SharePoint/Teams library;
  OneDrive is not a team archive.
- Retention policies in Purview keep content beyond that if required.

## Sequence that avoids data loss
1. Disable sign-in and revoke sessions.
2. Convert mailbox / apply hold; grant access; set auto-reply.
3. Hand over OneDrive files.
4. Remove licences (after step 2 is confirmed working).
5. Delete the user at the agreed date (deleted users are recoverable for 30 days).

## Gotchas
- Removing the licence before conversion or hold can start mailbox deletion after the
  grace period.
- Mailboxes with an archive or over 50 GB still need a licence as shared.
- Litigation hold requires an appropriate licence while the user is licensed.

## Verify
The manager can open the shared mailbox and OneDrive files, `Get-Mailbox -InactiveMailboxOnly`
lists the mailbox where a hold was used, and licences are released.
