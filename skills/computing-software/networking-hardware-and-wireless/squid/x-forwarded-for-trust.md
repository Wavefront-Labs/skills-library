---
id: computing-software.networking-hardware-and-wireless.squid.x-forwarded-for-trust
name: x-forwarded-for-trust
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, follow-x-forwarded-for, indirect-client, trusted-proxy, acl-uses-indirect-client]
level: advanced
status: docs-checked
description: "Trust upstream proxies to report real client IPs with follow_x_forwarded_for and the *_uses_indirect_client switches."
sources:
  - https://www.squid-cache.org/Doc/config/follow_x_forwarded_for/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# follow_x_forwarded_for
Needs `--enable-follow-x-forwarded-for`. Default: the header is ignored. Squid checks the X-Forwarded-For values in reverse, continuing while each matches an allow rule; the result is the indirect client address.
```
acl localhost src 127.0.0.1
acl my_other_proxy srcdomain .proxy.example.com
follow_x_forwarded_for allow localhost
follow_x_forwarded_for allow my_other_proxy
```
Apply the address with `acl_uses_indirect_client`, `icap_uses_indirect_client`, `delay_pool_uses_indirect_client`, `log_uses_indirect_client`, `tproxy_uses_indirect_client`.

Security: a trusted proxy can supply false client addresses, letting clients bypass source-based rules.

## Checked

2026-11-04. Read the follow_x_forwarded_for directive page and confirmed the build option, default, reverse-order checking, indirect client address, the five *_uses_indirect_client options, the security warning and the example. Nothing was removed.

Method: documentation only; no commands were run.
