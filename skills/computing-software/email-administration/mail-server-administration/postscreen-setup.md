---
id: computing-software.email-administration.mail-server-administration.postscreen-setup
name: postscreen-setup
category: computing-software
field: email-administration
product: mail-server-administration
tags: [postscreen-setup, postfix-postscreen, postscreen-access-list]
level: advanced
status: draft
description: "Enable postscreen in front of smtpd in master.cf to block zombie clients before they reach the SMTP daemon."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Postscreen setup

**Goal:** cheap connection-level screening (POSTSCREEN_README).
## Steps
1. In master.cf make `smtp inet ... postscreen`, add `smtpd pass ... smtpd`, `dnsblog unix ... dnsblog`, `tlsproxy unix ... tlsproxy` (lines as shipped in the sample master.cf).
2. `postscreen_access_list = permit_mynetworks`.
3. `postscreen_greet_action = enforce`; `postscreen_bare_newline_enable = yes`.
4. Restart (not just reload) Postfix after changing master.cf service types.
## Failure modes
- Authenticated clients on port 25 are screened too; move users to submission.
- Allowlisted clients are cached in `postscreen_cache_map`; temp file locking issues need a single writer (proxy service).
## Verify
- Log shows `postfix/postscreen` lines `CONNECT`, `PASS NEW` or `NOQUEUE: reject ... DNSBL`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
