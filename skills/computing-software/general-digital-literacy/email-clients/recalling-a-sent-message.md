---
id: computing-software.general-digital-literacy.email-clients.recalling-a-sent-message
name: recalling-a-sent-message
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email, compose, recall-message, undo-send, replace-message]
level: intro
status: docs-checked
description: "Recall or replace a sent email in Outlook for Microsoft 365 or Exchange accounts, use Gmail Undo Send, and know when recall cannot work so you send a correction."
sources:
  - https://support.microsoft.com/en-us/outlook/mail/how-to-recall-an-email-in-outlook-requirements-limitations-steps
  - https://support.google.com/mail/answer/2819488
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Recall or replace a sent message

## Outlook recall: strict conditions
- You can recall from new or classic Outlook for Windows or Outlook on the web only if you and the recipient both have a Microsoft 365 work or school email account in the same organisation, and the recipient has not opened the message yet.
- Personal accounts (Gmail, Hotmail, Outlook.com) cannot use message recall. Microsoft points personal accounts to the **Undo Send** delay in new Outlook for Windows or Outlook.com. Outlook for Mac has its own page.
- **New Outlook:** Sent Items > double-click the message to open it in its own window > ribbon **Recall Message** > OK. A Message Recall Report arrives in your inbox; its link shows whether the recall succeeded, is pending or failed.
- **Classic Outlook:** open the sent message, then Message tab > Move group > More Move Actions > **Recall This Message** (Simplified Ribbon: More commands > Actions > Recall This Message). If the command is missing you probably have no Exchange account or your organisation has not enabled it.

## Gmail Undo Send
- After Send, "Message sent" appears at bottom left with **Undo**.
- Set the window: Settings > See all settings > **Undo Send** > send cancellation period of 5, 10, 20 or 30 seconds > Save changes.

## If it cannot be recalled
Send a short correction ("Please disregard my previous email; the correct date is 14 May."). For a wrong recipient and sensitive data, ask them to delete it and follow your organisation's data-breach process.

## Verify
- [ ] The recall report shows success for each internal recipient, or a correction has been sent.

## Checked
2026-10-27. Microsoft Support "How to recall an email in Outlook" and Google Gmail Help "Send or unsend Gmail messages". Confirmed recall conditions, both Outlook paths, the report and the Gmail 5/10/20/30 second options. Removed unconfirmed Outlook.com undo-send duration, classic delayed-delivery rule and Apple Mail claims.
Method: documentation only; no commands were run.
