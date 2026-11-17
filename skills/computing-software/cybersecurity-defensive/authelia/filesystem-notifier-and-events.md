---
id: computing-software.cybersecurity-defensive.authelia.filesystem-notifier-and-events
name: filesystem-notifier-and-events
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, notifier, filesystem, notification-events, password-reset, testing, email-templates]
level: intro
status: docs-checked
description: "Use the filesystem notifier for testing and know which events Authelia notifies about, with the subjects and templates for each."
sources:
  - https://www.authelia.com/configuration/notifications/file/
  - https://www.authelia.com/configuration/notifications/events/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For tests, Authelia can write notifications to a file instead of sending email.

```yaml
notifier:
  disable_startup_check: false
  filesystem:
    filename: '/config/notification.txt'
```

The documentation says not to use this in production. It uses the plain-text email template, creates the file if missing, and treats an existing FIFO (named pipe) as a pipe, writing there instead. The operator must create the FIFO with `mkfifo` before Authelia starts, and a reader must be attached or the write blocks. The filesystem notifier delivers only the plaintext rendering, preceded by a header naming date, recipient and subject, and sends the user nothing.

Events Authelia notifies on, with their subject and template:

- Password reset requested: `Reset your password` (`IdentityVerificationJWT`).
- Session elevation requested: `Confirm your identity` (`IdentityVerificationOTC`).
- Password reset completed (after the reset flow) and password changed (user changes their own password in settings): both `Password changed successfully` (`Event`).
- Second factor registered: `Second Factor Method Added` (`Event`).
- Second factor removed: `Second Factor Method Removed` (`Event`).

There are no marketing, digest or administrative messages and no per-event switch to turn individual notifications off. Subject text is also used as the `{{ .Title }}` placeholder in a template.

Password reset notifications look identical from the requester's perspective whether or not the user exists, to prevent user enumeration; no message is sent for a nonexistent user.

Check: trigger a password reset with the filesystem notifier and read the link from the file.

## Checked

2026-11-08. Read in full: notifications/file, notifications/events. Corrected event list (password reset completed and password changed are separate events), added FIFO requirements and plaintext-only delivery.

Method: documentation only; no commands were run.
