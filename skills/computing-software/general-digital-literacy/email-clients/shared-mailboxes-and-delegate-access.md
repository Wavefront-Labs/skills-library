---
id: computing-software.general-digital-literacy.email-clients.shared-mailboxes-and-delegate-access
name: shared-mailboxes-and-delegate-access
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-account-setup, shared-mailbox, delegate-access, send-as, gmail-delegation]
level: practitioner
status: docs-checked
description: "Open a Microsoft 365 shared mailbox in Outlook and send from it, and give a delegate access to Gmail with the correct limits and invitation steps."
sources:
  - https://support.microsoft.com/en-us/outlook/sharing/open-and-use-a-shared-mailbox-in-outlook
  - https://support.google.com/mail/answer/138350
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Shared mailboxes and delegate access

## Microsoft 365 shared mailbox (info@, office@)
- Your IT admin must create the mailbox and add you as a member before you can use it.
- **New Outlook:** after you are added, restart Outlook; if it does not appear, right-click your account name in the folder pane > **Add shared folder or mailbox** and type the address. It shows as a subfolder under **Shared with me**.
- **Classic Outlook:** close and restart Outlook; the shared mailbox should appear in the folder pane. If not, add it manually in account settings.
- **Send from it:** New mail; if there is no From field, Options > **Show From** (classic: Options > From); choose the shared address, or Other email address and type it.

## Gmail delegation (computer only)
- Settings > See all settings > **Accounts and Import** > **Grant access to your account** > **Add another account** > enter the address > Send email to grant access. You cannot add delegates from the Gmail app, and you must verify your identity first.
- A delegate can read, send and delete mail but cannot chat or change your password; when they send, their own address appears. Personal accounts allow up to 10 delegates; work or school accounts up to 1,000.
- The invitation expires after a week; access can take up to 24 hours (up to an hour in some cases).
- The delegate opens the inbox from the profile picture account menu (marked Delegated); they should not bookmark the delegated inbox. Remove a delegate with Delete in the same setting.
- Delegates cannot use some features, including Gemini in Gmail, Smart Compose, Meet in Gmail and Add to Tasks.

## Verify
- [ ] Each member can open the shared mailbox and send a test from its address; delegates can open the delegated inbox.

## Checked
2026-10-27. Microsoft Support "Open and use a shared mailbox in Outlook" and Google Gmail Help "Delegate and collaborate on email". Confirmed the paths, limits and capabilities above. Removed unconfirmed Full Access/Send As terms, automapping steps, Outlook delegate menus, sent-items and rule claims.
Method: documentation only; no commands were run.
