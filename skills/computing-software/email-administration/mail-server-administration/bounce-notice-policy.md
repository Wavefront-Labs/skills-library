---
id: computing-software.email-administration.mail-server-administration.bounce-notice-policy
name: bounce-notice-policy
category: computing-software
field: email-administration
product: mail-server-administration
tags: [bounce-notice-policy, notify-classes, bounce-notice-recipient, bounce-template]
level: advanced
status: docs-checked
description: "Control which bounce notices Postfix sends with notify_classes, bounce_notice_recipient and 2bounce handling."
sources:
  - https://www.postfix.org/postconf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bounce notice policy

**Goal:** the postmaster sees problems without being flooded.
## Steps
1. `notify_classes = resource, software` (default) and add `bounce` or `2bounce` temporarily when debugging.
2. `postmaster` receives copies according to those classes (BASIC_CONFIGURATION: postmaster mail).
3. Set `bounce_size_limit` to cap returned content.
4. Customize wording with `bounce_template_file` if required.
## Failure modes
- The `bounce` class sends the postmaster headers of bounced mail and SMTP transcripts of rejected mail, so keep it for debugging only.
- Reject unknown recipients at SMTP time rather than accepting then bouncing (see ADDRESS_CLASS_README on backscatter).
## Verify
- Send to a nonexistent local user; expect the SMTP-time reject, not a later bounce.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): postconf(5) notify_classes, bounce_size_limit, bounce_template_file, ADDRESS_CLASS_README.
Confirmed: `notify_classes` default `resource, software`, `bounce` implies `2bounce`, `bounce_size_limit` (default 50000), `bounce_template_file`.
Corrected or removed: the flooding claim (replaced with what the `bounce` class sends).
Method: documentation only; no commands were run.
