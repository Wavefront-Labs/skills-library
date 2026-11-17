---
id: computing-software.email-administration.mail-server-administration.fail2ban-for-mail
name: fail2ban-for-mail
category: computing-software
field: email-administration
product: mail-server-administration
tags: [fail2ban-for-mail, fail2ban, brute-force, sasl-bruteforce]
level: practitioner
status: draft
description: "Use fail2ban jails for Postfix SASL and Dovecot to ban brute-force sources, with sane findtime and bantime."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fail2ban for mail

**Goal:** slow credential stuffing.
## Steps
1. Enable the shipped `postfix` (or `postfix[mode=aggressive]`) and `dovecot` jails; point `logpath` to the right log.
2. Set `maxretry = 5`, `findtime = 10m`, `bantime = 1h` (adjust; use incremental bantime).
3. Whitelist your own addresses with `ignoreip`.
## Failure modes
- Banning a NATed office; check before banning large ranges.
- Log format changes break filters.
## Verify
- `fail2ban-client status dovecot` shows banned IPs after a test failure series from a lab host.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
