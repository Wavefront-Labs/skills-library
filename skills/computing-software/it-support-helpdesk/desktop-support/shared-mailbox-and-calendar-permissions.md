---
id: computing-software.it-support-helpdesk.desktop-support.shared-mailbox-and-calendar-permissions
name: shared-mailbox-and-calendar-permissions
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, microsoft-365, m365-support, mailbox-permissions, shared-mailbox, full-access, send-as, send-on-behalf, calendar-permissions, add-mailboxpermission, exchange-online-powershell, automapping, delegate]
level: practitioner
status: docs-checked
description: "Grant and troubleshoot Exchange Online access: shared mailbox Full Access, Send As vs Send on Behalf, automapping, calendar folder permissions and delegates."
sources:
  - "https://learn.microsoft.com/en-us/microsoft-365/admin/email/create-a-shared-mailbox"
  - "https://learn.microsoft.com/en-us/powershell/module/exchange/add-mailboxpermission"
  - "https://learn.microsoft.com/en-us/powershell/module/exchange/add-mailboxfolderpermission"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# shared-mailbox-and-calendar-permissions

Goal: give the right person exactly the access the request approved, and fix "I can see it but can't send" tickets.

## Shared mailbox permissions
- **Full Access**: open the mailbox and act as its owner (read, delete, change mail, create calendar items and
  tasks). It does not allow sending unless the user also has Send As or Send on Behalf.
- **Send As**: mail looks like the shared mailbox sent it.
- **Send on Behalf**: mail shows "John on behalf of Reception Building 32". Grant it in the EAC or with the
  `Set-Mailbox` cmdlet's GrantSendOnBehalf parameter.
- EAC: Recipients > Mailboxes > select the mailbox > Edit > Mailbox permissions > Manage mailbox delegation, to
  add or remove Full Access and Send As. Microsoft states both are required for the shared mailbox to operate.
- Send As and Send on Behalf do not work in Outlook desktop when `HiddenFromAddressListsEnabled` is True on the
  mailbox, because they need the mailbox visible in the Global Address List.
- New shared mailboxes have sign-in blocked by default.
- Shared mailboxes usually need no licence. An Exchange Online Plan 2 licence is required when the mailbox has more
  than 50 GB in use, uses in-place archiving, or is on litigation hold.
- A shared mailbox includes a shared calendar visible to its members.

```powershell
Add-MailboxPermission -Identity sales@contoso.com -User jo@contoso.com -AccessRights FullAccess -InheritanceType All -AutoMapping $true
```
`-AutoMapping $false` stops the mailbox appearing automatically in Outlook.

## Automapping
- Automapping is on by default and is set on the user's mailbox, not the shared one. The shared mailbox appears in
  Outlook after the user closes and restarts it.
- Granting access through a security group means automapping will not work: assign permissions explicitly.

## Calendar
```powershell
Add-MailboxFolderPermission jo@contoso.com:\Calendar -User pa@contoso.com -AccessRights Editor -SharingPermissionFlags Delegate
```
- Roles on the page include `AvailabilityOnly` (availability only), `LimitedDetails` (availability with subject
  and location), `Reviewer` (FolderVisible, ReadItems) and `Editor` (create, edit and delete items).
- `-SharingPermissionFlags Delegate` makes the user a calendar delegate, including receiving meeting invites and
  responses. `CanViewPrivateItems` gives private-item access and must be used together with `Delegate`.

## Gotchas
Mailbox access is data access. Record the approver (mailbox owner or manager) in the ticket; remove access in leaver
and mover processes.

## Verify
The user opens the mailbox in Outlook and OWA and sends a test as or on behalf; the permission list shows exactly
the intended entries.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the shared mailbox article and the Add-MailboxPermission and Add-MailboxFolderPermission references.
Removed because the pages do not state them: Add-RecipientPermission and Get-*Permission audit commands, replication
time, Set-MailboxFolderPermission example, Sent-items copy settings, localised calendar folder names, and the role
ordering.
