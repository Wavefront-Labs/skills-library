---
id: computing-software.email-administration.mail-server-administration.mta-sts-policy-file
name: mta-sts-policy-file
category: computing-software
field: email-administration
product: mail-server-administration
tags: [mta-sts-policy-file, mta-sts-tls-rpt, mta-sts, mta-sts-policy, _mta-sts]
level: advanced
status: docs-checked
description: "Publish an MTA-STS policy over HTTPS plus the _mta-sts TXT record, starting in testing mode."
sources:
  - https://www.rfc-editor.org/rfc/rfc8461
  - https://www.rfc-editor.org/rfc/rfc8460
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mta sts policy file

**Goal:** tell senders to require TLS with valid certs for your MX (RFC 8461).
## Steps
1. Serve `https://mta-sts.example.com/.well-known/mta-sts.txt` over HTTPS (the policy host must be `mta-sts.` plus the policy domain):
```
version: STSv1
mode: testing
mx: mail.example.com
max_age: 86400
```
2. DNS: `_mta-sts.example.com. TXT "v=STSv1; id=20261102a"`. The `id` is 1 to 32 letters or digits.
3. Change `id` whenever the policy changes, and update the HTTPS policy body before updating the TXT record.
4. Modes: `testing` lets mail be delivered as if there were no validation failure (senders that implement TLS reporting send a report); `enforce` forbids delivery to hosts that fail MX matching, certificate validation or do not support STARTTLS; `none` is for opting out. Move to `enforce` after the reports are clean.
5. `max_age` is in seconds with a maximum of 31557600. The RFC expects the value typically to be weeks or greater for a live policy.
## Failure modes
- If a valid TXT record exists but the policy cannot be fetched over HTTPS (for example a bad certificate), senders cannot get the policy.
- `mx` patterns that do not match the real MX hosts: in enforce mode senders will not deliver to the non-matching hosts.
## Verify
- `curl -s https://mta-sts.example.com/.well-known/mta-sts.txt`; `dig +short TXT _mta-sts.example.com`.

## Checked

2026-11-09. Confirmed on RFC 8461: the well-known path and policy host, policy fields version, mode, mx and max_age (maximum 31557600, typically weeks or greater), the TXT record format and id syntax, the three modes, the update order for the policy body and TXT record, and the opt-out workflow using mode none. RFC 8460 was used only for the testing mode report link. Removed: the "enforce defers mail" wording, which the RFC phrases as MUST NOT deliver, and the boilerplate Postfix/Dovecot notes.

Method: documentation only; no commands were run.
