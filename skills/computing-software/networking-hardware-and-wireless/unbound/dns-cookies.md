---
id: computing-software.networking-hardware-and-wireless.unbound.dns-cookies
name: dns-cookies
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, dns-cookies, allow-cookie, cookie-secret, anycast, ratelimit-cookie]
level: advanced
status: docs-checked
description: "Use DNS Cookies in Unbound: allow_cookie access control, cookie-aware limits, and the unbound-control secret rollover procedure for anycast nodes."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dns cookies
Config effects:
- `access-control: <netblock> allow_cookie` (UDP only) requires a valid Cookie.
- `ip-ratelimit` is bypassed by clients with a valid Cookie; `ip-ratelimit-cookie` sets a separate limit, suggested about tenfold.
- `wait-limit-cookie` (10000) replaces `wait-limit` (1000) for cookie-bearing clients.
- `cookie-secret-file` (default empty, meaning disabled) persists secrets.

Secret commands:
- `add_cookie_secret secret` takes a 128-bit hex string. With no active secret it becomes active; otherwise it becomes (or replaces) the staging secret.
- `activate_cookie_secret` swaps staging and active.
- `drop_cookie_secret` removes the staging secret.
- `print_cookie_secrets` shows secrets and status.
Verification accepts the active or staging secret.

Rollover on anycast nodes: add as staging on all nodes, activate once all have it, keep it active at least one hour, then drop the old secret.

Counters: `num.queries_cookie_valid`, `_cookie_client`, `_cookie_invalid`.

## Checked
2026-11-04. Confirmed against the unbound.conf manual and unbound-control manual: cookie secret commands, staging/active behaviour, anycast rollover with the one-hour wait, wait-limit-cookie and ip-ratelimit-cookie. Nothing removed.
Method: documentation only; no commands were run.
