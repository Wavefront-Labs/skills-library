---
id: computing-software.general-digital-literacy.email-clients.sending-large-files-as-links
name: sending-large-files-as-links
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, attachments, attach-vs-link, large-attachments, onedrive-link, google-drive-link, wetransfer, attachment-size-limit, file-size-limits]
level: intro
status: docs-checked
description: "Know the Gmail 25 MB attachment limit and Exchange Online defaults, and send big files as cloud links instead of bouncing attachments."
sources:
  - https://support.google.com/mail/answer/6584
  - https://learn.microsoft.com/en-us/office365/servicedescriptions/exchange-online-service-description/exchange-online-limits
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sending large files as cloud links

**Goal:** get a big file to someone without bounced emails.

## Limits
- **Gmail, personal accounts:** attachments up to 25 MB. If the total is over the limit, Gmail removes the attachment and adds it as a Google Drive link. For work or school accounts, the Workspace administrator sets sending and receiving limits. Gmail does not let you attach executable files such as .exe. Attachments count toward your Google storage; if storage is full you cannot send or receive attachments.
- **Microsoft 365 / Exchange Online:** the default maximum message size is 35 MB for sending and 36 MB for receiving, including attachments; administrators can set a custom limit between 1 MB and 150 MB. Some email clients have lower limits, and over-size messages are not delivered (the sender gets a non-delivery report).
- The size you can send also depends on the recipient's server and client; for big files prefer a link.

## Send a link instead
- Upload to your cloud storage (Google Drive, OneDrive or similar) and paste a share link, choosing who can open it (specific people, or anyone with the link) and view or edit access.
- Zip many files first so it is one download.

## Gotchas
- A link to a file you later delete or move stops working; keep it until they have downloaded.
- Anyone-with-the-link access can be forwarded; use specific people for confidential files.

## Verify
- [ ] Open the link in a private window: you get the access level you intended, or a sign-in prompt.

## Checked
2026-10-27. Google Gmail Help "Send attachments with your Gmail message" and Microsoft Learn "Exchange Online limits". Confirmed the Gmail limit, Drive link behaviour, storage and executable rules, and Exchange Online defaults. Removed unconfirmed Gmail 50 MB receive limit, Outlook.com 20 MB, encoding-overhead, Mail Drop and step-by-step link menus.
Method: documentation only; no commands were run.
