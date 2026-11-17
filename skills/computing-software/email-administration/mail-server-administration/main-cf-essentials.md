---
id: computing-software.email-administration.mail-server-administration.main-cf-essentials
name: main-cf-essentials
category: computing-software
field: email-administration
product: mail-server-administration
tags: [main-cf-essentials, postfix-basics, main-cf, myhostname, mydestination, mynetworks, myorigin]
level: intro
status: docs-checked
description: "Set the Postfix main.cf essentials: myhostname, mydomain, myorigin, inet_interfaces, mydestination, mynetworks."
sources:
  - https://www.postfix.org/BASIC_CONFIGURATION_README.html
  - https://www.postfix.org/postconf.5.html
  - https://www.postfix.org/ADDRESS_CLASS_README.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Main cf essentials

**Goal:** a correct baseline from BASIC_CONFIGURATION_README.
## Steps
1. `postconf -e 'myhostname = mail.example.com'`, `mydomain = example.com`, `myorigin = $mydomain`.
2. `inet_interfaces = all` for a public MX; `loopback-only` for a send-only host.
3. `mydestination = $myhostname, localhost.$mydomain, localhost` (leave `$mydomain` out when using virtual domains).
4. `mynetworks = 127.0.0.0/8 [::1]/128` (or `mynetworks_style = host`).
5. `postfix check && postfix reload`.
## Failure modes
- A domain in both `mydestination` and `virtual_mailbox_domains`: address class conflict, misrouting.
- Editing main.cf without reload: changes are ignored.
## Verify
- `postconf -n` shows only your non-default settings and no typos.
- `postconf -d myorigin` shows the default for comparison (the postconf(5) default is `$myhostname`).

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): BASIC_CONFIGURATION_README, postconf(5), ADDRESS_CLASS_README.
Confirmed: `myhostname`, `mydomain`, `myorigin`, `inet_interfaces` (`all`, `loopback-only`), `mydestination` default `$myhostname, localhost.$mydomain, localhost`, `mynetworks`, `mynetworks_style` default `host` from 3.0, `postfix check`, `postfix reload`, address-class conflicts.
Corrected or removed: nothing wrong found; defaults added.
Method: documentation only; no commands were run.
