---
id: computing-software.email-administration.dovecot.proxy-passdb-fields-and-authentication-modes
name: proxy-passdb-fields-and-authentication-modes
category: computing-software
field: email-administration
product: dovecot
tags: [proxy-passdb, proxy-maybe, proxy-mech, login-trusted-networks, imap-capability, proxy-multiplexing]
level: advanced
status: docs-checked
description: "Proxy IMAP, POP3, submission, LMTP, ManageSieve and doveadm to backends using passdb extra fields, password forwarding or a master password."
sources:
  - https://doc.dovecot.org/main/core/config/proxy/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dovecot can proxy IMAP, POP3, submission, LMTP, ManageSieve and doveadm connections, for all users or selected ones. There are two ways to authenticate to the backend:

1. Forward the user's password or OAUTH token: return `pass=%{password}` and `proxy_mech=%{mechanism}`. This fails with non-cleartext, non-token mechanisms, which prevent password forwarding by design. `proxy_mech` is needed only when both OAUTH and cleartext mechanisms are enabled.
2. Log in with a master password: return `pass=master_secret`. The client may then use non-cleartext mechanisms too.

Enable proxying with the `proxy` or `proxy_maybe` extra field, plus the required `host` field. `proxy_maybe` supports mixed proxy and backend servers: if the destination matches the current connection, the user is logged in normally instead of proxied. `auth_proxy_self` lists extra IPs that count as the proxy's own.

Other fields: the destination `port` (143 for IMAP, 110 for POP3), the source IP for outgoing connections, `protocol` (lmtp or smtp, relevant to LMTP), `destuser` to change the login name, a SASL mechanism, and a timeout overriding `login_proxy_timeout` (login processes only).

On the backends set `login_trusted_networks` to the proxy IPs so real client IPs are logged. Backends need not run Dovecot, but make sure the proxy does not advertise more capabilities than the backend supports, for example with `imap_capability`. The IMAP proxy sends an updated untagged CAPABILITY if the backend differs, though some clients ignore it.

IMAP multiplexing is on by default between proxy and Dovecot backend; a passdb field can disable it per connection, which moves COMPRESS work to the backend.

## Checked

2026-11-03. Confirmed on the Dovecot Proxying page: supported protocols, the two authentication ways (pass=%{password} with proxy_mech, or pass=master_secret), proxy and proxy_maybe with required host, auth_proxy_self, the port defaults 143/110, source_ip, protocol (LMTP only), destuser, proxy_timeout overriding login_proxy_timeout, login_trusted_networks on backends, imap_capability and the updated CAPABILITY reply, and proxy_no_multiplex (added 2.4.0) moving COMPRESS work to the backend. Nothing removed.

Method: documentation only; no commands were run.
