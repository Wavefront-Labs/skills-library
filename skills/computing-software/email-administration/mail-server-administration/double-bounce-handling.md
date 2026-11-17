---
id: computing-software.email-administration.mail-server-administration.double-bounce-handling
name: double-bounce-handling
category: computing-software
field: email-administration
product: mail-server-administration
tags: [double-bounce-handling, double-bounce, 2bounce-notice-recipient]
level: advanced
status: docs-checked
description: "Handle double bounces (bounces that cannot be delivered) with double_bounce_sender, 2bounce_notice_recipient and discard policies."
sources:
  - https://www.postfix.org/postconf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Double bounce handling

**Goal:** do not loop, do not hoard.
## Facts
- A double bounce is a bounce notice that itself cannot be returned to the sender; when the `2bounce` class is enabled in `notify_classes` (the default is `resource, software`; `bounce` implies `2bounce`), Postfix sends it to `2bounce_notice_recipient` (default postmaster).
- `double_bounce_sender` (default `double-bounce`) is the sender of postmaster notifications; all mail to that address is silently discarded to end bounce loops.
## Steps
1. Point `2bounce_notice_recipient` at a monitored mailbox if you enable the `2bounce` class.
2. `postconf double_bounce_sender 2bounce_notice_recipient notify_classes` to inspect.
## Failure modes
- Accumulating double bounces in a mailbox nobody reads.
## Verify
- With `2bounce` enabled in staging, an undeliverable bounce should arrive at `2bounce_notice_recipient`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): postconf(5) notify_classes, 2bounce_notice_recipient, double_bounce_sender.
Confirmed: `2bounce_notice_recipient` default postmaster, `double_bounce_sender` default double-bounce, the 2bounce class.
Corrected or removed: the advice to alias `double-bounce@` to a mailbox (Postfix discards that mail by design) and the null-sender explanation.
Method: documentation only; no commands were run.
