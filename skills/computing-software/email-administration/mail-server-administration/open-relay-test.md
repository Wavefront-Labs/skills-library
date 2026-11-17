---
id: computing-software.email-administration.mail-server-administration.open-relay-test
name: open-relay-test
category: computing-software
field: email-administration
product: mail-server-administration
tags: [open-relay-test, postfix-open-relay, open-relay, relay-test]
level: practitioner
status: docs-checked
description: "Test your server from outside for open relay by attempting to relay mail to a third-party domain with manual SMTP."
sources:
  - https://www.postfix.org/postconf.5.html
  - https://www.postfix.org/VIRTUAL_README.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Open relay test

**Goal:** prove strangers cannot send through you.
## Steps
1. From a host outside mynetworks: `openssl s_client -starttls smtp -connect mail.example.com:25 -crlf`.
2. `EHLO test.example.net`, `MAIL FROM:<a@example.net>`, `RCPT TO:<b@example.org>` where example.org is not yours.
3. Expected: a rejection ("Relay access denied"). The default `smtpd_relay_restrictions` ends with `defer_unauth_destination`, which defers (4xx) unless you use `reject_unauth_destination`.
4. Also test `RCPT TO:<b%example.org@example.com>`: `allow_percent_hack` defaults to yes, so check how your build treats it.
## Failure modes
- A success (2xx) reply on the third-party RCPT means open relay: fix before anything else.
- Testing from inside mynetworks gives a false pass.
## Verify
- The mail log shows a reject or defer for that RCPT.
- Re-test after any change to restrictions or `mynetworks`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): postconf(5) smtpd_relay_restrictions, allow_percent_hack, VIRTUAL_README.
Confirmed: default `smtpd_relay_restrictions` (`permit_mynetworks, permit_sasl_authenticated, defer_unauth_destination`), `allow_percent_hack` default yes, 'relay access denied' reject wording.
Corrected or removed: the fixed 554 5.7.1 reply (default config defers), the NOQUEUE log string, the quoted-address trick.
Method: documentation only; no commands were run.
