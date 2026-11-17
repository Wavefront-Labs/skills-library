---
id: computing-software.email-administration.mail-server-administration.mynetworks-hardening
name: mynetworks-hardening
category: computing-software
field: email-administration
product: mail-server-administration
tags: [mynetworks-hardening, trusted-networks]
level: practitioner
status: docs-checked
description: "Keep mynetworks minimal and avoid trusting whole subnets or cloud NAT ranges that other tenants share."
sources:
  - https://www.postfix.org/postconf.5.html
  - https://www.postfix.org/BASIC_CONFIGURATION_README.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mynetworks hardening

**Goal:** only hosts you control get relay without auth.
## Steps
1. `postconf mynetworks mynetworks_style` to see the effective trust.
2. Set explicit: `mynetworks = 127.0.0.0/8 [::1]/128 192.0.2.10/32`.
3. Prefer authenticated submission for all other senders (see submission-port-587).
4. Remember `permit_mynetworks` also trusts containers behind a proxy that rewrites source addresses.
## Failure modes
- `mynetworks_style = subnet` trusts the whole connected subnet (default is `host` from Postfix 3.0); a large subnet trusts many hosts.
- A reverse proxy or NAT makes every client look local and unlocks relay for the internet.
## Verify
- Run open-relay-test from a host in the same provider network but outside the list.
- `postconf -n | grep mynetworks` shows what you intended.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): postconf(5) mynetworks, mynetworks_style, BASIC_CONFIGURATION_README (NAT/proxy section).
Confirmed: `mynetworks` and `mynetworks_style` behaviour and defaults, NAT/proxy clients appearing as the proxy address.
Corrected or removed: the '/16 trusts thousands' wording (made general).
Method: documentation only; no commands were run.
