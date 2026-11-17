---
id: computing-software.general-digital-literacy.email-clients.read-and-delivery-receipts
name: read-and-delivery-receipts
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email, compose, read-receipt, delivery-receipt, tracking-pixels]
level: intro
status: docs-checked
description: "Request read and delivery receipts in Outlook and Gmail, respond to requests, and understand which accounts support them and why a receipt proves little."
sources:
  - https://support.microsoft.com/en-us/outlook/mail/add-and-request-read-receipts-and-delivery-notifications-in-outlook
  - https://support.google.com/mail/answer/9413651
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Read and delivery receipts

## Request
- **New Outlook:** in a message, Options tab > Tracking group > **Request a Delivery Receipt** and/or **Request a Read Receipt** (use More Options if hidden).
- **Classic Outlook:** File > Options > Mail > under Tracking tick Delivery receipt and/or Read receipt to request them for all messages.
- Microsoft notes receipts are not available for IMAP or POP accounts such as Gmail, Yahoo! or iCloud, and on Outlook.com accounts the feature needs a Microsoft 365 subscription. There is no way to force a recipient to send a read receipt.
- **Gmail:** read receipts work only with work or school accounts, not personal @gmail.com. Compose > More options > **Request read receipt** > Send. The recipient may need to approve it first.

## Respond
- Outlook (new, web, Outlook.com): Settings > Mail > Message handling > under Read receipts choose how to respond.
- Gmail (work or school): if your organisation wants approval, choose **Send receipts** or **Not now** (you will be asked next time you open the message). If you see no prompt, the receipt was sent automatically.

## Limits
- Gmail receipts are not returned for group mailing lists or aliases, when an admin restricts them, or for recipients on clients that do not sync in real time (some POP or sync clients) or that do not send IMAP receipts automatically.
- A receipt does not prove a person read the message: an IMAP client that marks it read can trigger one, and some mobile systems never return receipts. Google advises against relying on receipts to certify delivery.
- For formal notices, ask for a reply in the text.

## Verify
- [ ] For a formal notice, a reply or acknowledgement is requested in the text, not only a receipt.

## Checked
2026-10-27. Microsoft Support "Add and request read receipts and delivery notifications in Outlook" and Google Gmail Help "Request or return a read receipt". Confirmed the paths, account restrictions and limits above. Removed unconfirmed Apple Mail and tracking-pixel claims.
Method: documentation only; no commands were run.
