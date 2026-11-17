---
id: computing-software.email-administration.mail-server-administration.clamav-scanning
name: clamav-scanning
category: computing-software
field: email-administration
product: mail-server-administration
tags: [clamav-scanning, malware-scanning, clamav, clamd, freshclam, antivirus]
level: practitioner
status: draft
description: "Scan mail with ClamAV via clamd and clamav-milter or Rspamd antivirus, keep signatures updated with freshclam."
sources:
  - https://docs.clamav.net/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clamav scanning

**Goal:** reject known malware at SMTP time.
## Steps
1. Install clamd and enable `freshclam` for signature updates.
2. Postfix: add clamav-milter to `smtpd_milters` (or enable Rspamd's antivirus module pointing at the clamd socket).
3. Set `MaxFileSize` and `StreamMaxLength` in clamd.conf; ensure Postfix `message_size_limit` is not larger.
4. Ensure clamd has enough memory (databases load into RAM).
## Failure modes
- clamd out of memory or signature update failing: scanner stops silently.
- Scanning encrypted archives is not possible.
## Verify
- Test with the EICAR string (a harmless test file): the message is rejected.
- `freshclam` log shows recent updates.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
