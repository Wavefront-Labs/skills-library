---
id: computing-software.email-administration.mail-server-administration.dsn-reading
name: dsn-reading
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dsn-reading, bounces-dsn, dsn, delivery-status-notification, diagnostic-code]
level: practitioner
status: docs-checked
description: "Read a delivery status notification: reporting MTA, final recipient, action, Status and Diagnostic-Code fields."
sources:
  - https://www.rfc-editor.org/rfc/rfc3464
  - https://www.rfc-editor.org/rfc/rfc3463
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dsn reading

**Goal:** extract the real cause from a bounce (RFC 3464).
## Steps
1. Open the `message/delivery-status` part of the bounce. It has per-message fields (such as `Reporting-MTA` and `Original-Envelope-Id`) followed by per-recipient fields.
2. Read `Final-Recipient`, `Action`, `Status` (x.y.z) and `Diagnostic-Code`. `Action` is one of failed, delayed, delivered, relayed or expanded. `expanded` means delivery to an alias with onward forwarding and is not a terminal state, so further failed or delayed notices may follow.
3. Map `Status` using RFC 3463 (for example 5.1.1 is a bad destination mailbox address, 5.2.2 is mailbox full, 5.7.1 is delivery not authorized, message refused).
4. `Reporting-MTA` is not necessarily the MTA that actually experienced the problem; use `Diagnostic-Code` and the status to find who rejected it.
5. Cross-check the text with your own mail log for the same message.
## Failure modes
- `Final-Recipient` can differ from the address the sender originally used, for example after aliasing.
## Verify
- You can state who rejected it, at which stage, and the remedy.

## Checked

2026-11-09. Confirmed on RFC 3464: the message/delivery-status content type, the Original-Envelope-Id, Reporting-MTA, Final-Recipient, Action (failed, delayed, delivered, relayed, expanded) and Diagnostic-Code fields, the note on expanded, and that the Reporting-MTA is not necessarily the MTA that experienced the problem. Confirmed on RFC 3463 the X.1.1, X.2.2 and X.7.1 meanings. Removed: the backscatter paragraph (not in the RFC) and the boilerplate notes.

Method: documentation only; no commands were run.
