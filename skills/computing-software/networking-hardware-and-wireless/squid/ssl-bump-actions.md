---
id: computing-software.networking-hardware-and-wireless.squid.ssl-bump-actions
name: ssl-bump-actions
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, ssl-bump, splice, bump, peek, stare, terminate]
level: advanced
status: docs-checked
description: "Decide per connection whether Squid decrypts or tunnels TLS using ssl_bump actions splice, bump, peek, stare and terminate."
sources:
  - https://www.squid-cache.org/Doc/config/ssl_bump/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ssl_bump actions
Checked on a CONNECT to an `http_port` with `ssl-bump`, or on an intercepted connection. Requires OpenSSL. Syntax: `ssl_bump <action> [!]acl ...`. If no rule matches, Squid splices.

Actions:
- `splice`: TCP tunnel, no decryption (default)
- `bump`: decrypt, with a mimicked server certificate at SslBump2 or SslBump3
- `peek`: read the client (step 1) or server (step 2) certificate, keeping splice possible
- `stare`: same, keeping bump possible
- `terminate`: close both connections

Legacy, SslBump1 only: `client-first`, `server-first`, `peek-and-splice` (marked for removal), `none`.

Rules are evaluated at SslBump1, SslBump2 and SslBump3; impossible actions are ignored and the first match wins.

```
acl broken_sites ssl::server_name .example.com
ssl_bump splice localhost
ssl_bump splice broken_sites
ssl_bump bump all
```

## Checked

2026-11-04. Read the ssl_bump directive page and confirmed the default splice action, each action, the legacy SslBump1 actions, the all-steps evaluation rule and the example. Nothing was removed.

Method: documentation only; no commands were run.
