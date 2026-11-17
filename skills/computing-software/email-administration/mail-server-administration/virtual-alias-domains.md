---
id: computing-software.email-administration.mail-server-administration.virtual-alias-domains
name: virtual-alias-domains
category: computing-software
field: email-administration
product: mail-server-administration
tags: [virtual-alias-domains, postfix-virtual, virtual-alias-domain, virtual-alias-maps]
level: practitioner
status: draft
description: "Host a domain whose addresses are all aliases to other addresses using virtual_alias_domains and virtual_alias_maps."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Virtual alias domains

**Goal:** accept mail for example.org and forward each address elsewhere (VIRTUAL_README).
## Steps
1. `virtual_alias_domains = example.org`
2. `virtual_alias_maps = hash:/etc/postfix/virtual`
3. In the table: `info@example.org  alice@example.com` and a catch-all `@example.org  bob@example.com`.
4. `postmap /etc/postfix/virtual && postfix reload`.
## Failure modes
- Domain listed also in `mydestination`: conflict.
- Catch-all swallows typos and spam; prefer explicit entries.
- Forgetting `postmap` after editing: the old table stays in effect.
## Verify
- `postmap -q info@example.org hash:/etc/postfix/virtual` prints the target.
- `postmap -q @example.org hash:/etc/postfix/virtual` checks the catch-all.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
