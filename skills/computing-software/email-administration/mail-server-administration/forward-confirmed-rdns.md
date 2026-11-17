---
id: computing-software.email-administration.mail-server-administration.forward-confirmed-rdns
name: forward-confirmed-rdns
category: computing-software
field: email-administration
product: mail-server-administration
tags: [forward-confirmed-rdns, fcrdns, forward-confirmed-reverse-dns]
level: practitioner
status: draft
description: "Check forward-confirmed reverse DNS (FCrDNS): PTR name resolves back to the same IP, matching HELO."
sources:
  - https://www.rfc-editor.org/rfc/rfc5321
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Forward confirmed rdns

**Goal:** IP -> PTR name -> same IP, and the HELO/EHLO name agrees.
## Steps
1. `ip=192.0.2.25; name=$(dig +short -x $ip | head -1); echo $name`
2. `dig +short A $name` must contain the IP (use AAAA for IPv6).
3. Set Postfix `smtp_helo_name = mail.example.com` (defaults to `myhostname`) so outbound HELO matches.
4. Make sure the TLS certificate on port 25 covers that name (tidy, not required).
## Failure modes
- PTR set but forward A missing or pointing to a different IP.
- NAT or shared egress: outbound IP differs from the server's public listener IP.
- Several outbound IPs with one HELO name: each IP needs a matching PTR/A pair.
## Verify
- Receiver headers show the connecting host name rather than "unknown".
- `postconf smtp_helo_name myhostname` shows the intended name.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
