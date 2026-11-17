---
id: computing-software.email-administration.dovecot.secured-connection-rules-and-haproxy
name: secured-connection-rules-and-haproxy
category: computing-software
field: email-administration
product: dovecot
tags: [secured-connection, haproxy-tls, login-trusted-networks, localhost, cleartext-auth, secured-variable]
level: advanced
status: docs-checked
description: "Which connections Dovecot treats as secured, including HAProxy TLS termination, localhost and login_trusted_networks, and how ssl required changes that."
sources:
  - https://doc.dovecot.org/main/core/config/ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `ssl` value influences whether a connection counts as secured. A secured connection may always use plaintext authentication, and auth lookups mark it so, which sets the `%{secured}` variable.

Always secured:
- Connections whose TLS Dovecot itself terminates.
- Connections HAProxy marks as TLS, even if HAProxy runs on another host and the link to Dovecot is unprotected. The reasoning is that such a layout is deliberate, and refusing it would make `ssl = required` impossible to enforce for end clients.
- Client-to-HAProxy connections on localhost, again regardless of the HAProxy to Dovecot hop.
- Non-HAProxy connections from localhost.

Secured only when `ssl` is not `required`:
- Other connections from `login_trusted_networks`.
- Other connections coming through HAProxy.

Practical consequence: with `ssl = required`, connections from `login_trusted_networks` and other HAProxy connections no longer count as secured, while connections HAProxy marks as TLS still do.

## Checked
2026-11-09. Read the Dovecot core/config/ssl page (Secured Connections section). Confirmed the secured-connection
list, the `ssl = required` exception, the HAProxy reasoning, plaintext authentication on secured connections and the
`%{secured}` variable. Removed as unconfirmed: the advice to use `%{secured}` in passdb or userdb logic and the proxy
certificate-management remark.
Method: documentation only; no commands were run.
