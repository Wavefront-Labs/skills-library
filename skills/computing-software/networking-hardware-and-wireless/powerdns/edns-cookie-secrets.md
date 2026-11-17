---
id: computing-software.networking-hardware-and-wireless.powerdns.edns-cookie-secrets
name: edns-cookie-secrets
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, edns-cookie, edns-cookie-secret, pdns-control, rfc9018, secret-rollover]
level: practitioner
status: docs-checked
description: "Manage PowerDNS EDNS cookie secrets: edns-cookie-secret format, pdns_control cookie-secret list/add/delete, BADCOOKIE behaviour, rolling secrets, persistence."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/guides/edns-cookies.rst
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/pdns_control.1.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EDNS cookie secrets

Setting `edns-cookie-secret` must be exactly 32 hexadecimal characters (a 128-bit SipHash key). From 5.2.0 it may be a comma-separated list: the first secret creates new cookies, all of them validate. PowerDNS implements RFC 9018 and does not roll secrets itself.

Runtime, no restart:
```
pdns_control cookie-secret list
pdns_control cookie-secret add <32-hex|random>
pdns_control cookie-secret delete <32-hex|last>
```
`list` marks the active secret with `*`. `add` makes the new one active. `delete` removes an inactive secret; `last` targets the oldest.

Behaviour:
- An expired, non-validating or client-only cookie gets BADCOOKIE (RFC 7873) and a fresh server cookie.
- A valid cookie made with an older secret is processed normally, and the reply carries a new cookie from the active secret.

Rolling: RFC 7873 asks for updates at least every 36 days. The page suggests a weekly cron or systemd timer running `add random`, then later `delete last`.

Caveats:
- Runtime changes are not written to the config; after a restart PowerDNS reads the secrets from the config file, so other plumbing may be needed to keep it in sync.

## Checked

2026-11-04. Read guides/edns-cookies.rst in full and confirmed the 32-hex secret, 5.2.0 list form, cookie-secret list/add/delete behaviour, BADCOOKIE rule, 36-day RFC 7873 requirement, weekly roll suggestion and the restart note. Removed an unsupported remark about the */7 cron field.

Method: documentation only; no commands were run.
