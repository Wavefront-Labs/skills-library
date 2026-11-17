---
id: computing-software.email-administration.mail-server-administration.milter-integration
name: milter-integration
category: computing-software
field: email-administration
product: mail-server-administration
tags: [milter-integration, postfix-milter, smtpd-milters, non-smtpd-milters]
level: advanced
status: docs-checked
description: "Attach milters (DKIM signing, Rspamd) to Postfix with smtpd_milters and non_smtpd_milters over a socket."
sources:
  - https://www.postfix.org/MILTER_README.html
  - https://www.postfix.org/postconf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Milter integration

**Goal:** run external filters via the milter protocol (MILTER_README).
## Steps
1. `smtpd_milters = inet:127.0.0.1:11332` (or `unix:/run/rspamd/milter.sock`).
2. `non_smtpd_milters = $smtpd_milters` so locally submitted mail is processed too.
3. `milter_default_action = tempfail` (fail closed) or `accept` (fail open).
4. `milter_protocol` (default 6), then `postfix reload`.
## Failure modes
- Wrong socket permissions or chroot path: Postfix cannot connect; a chrooted smtpd or cleanup process needs a path valid inside the chroot (MILTER_README), and the `milter_default_action` result applies.
- Milters are called in the order configured (MILTER_README), so list the one that must see the final message last.
## Verify
- Added headers or a milter reject show it ran; confirm the milter is listening on the configured address.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): MILTER_README, postconf(5).
Confirmed: `smtpd_milters`, `non_smtpd_milters` (default empty), `inet:` and `unix:` address forms, `milter_default_action`, `milter_protocol` default 6, configured-order calling, chroot path note.
Corrected or removed: the milter-reject log string and the DKIM-ordering rationale (replaced with documented order rule).
Method: documentation only; no commands were run.
