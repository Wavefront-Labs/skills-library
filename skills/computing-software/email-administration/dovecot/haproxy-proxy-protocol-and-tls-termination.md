---
id: computing-software.email-administration.dovecot.haproxy-proxy-protocol-and-tls-termination
name: haproxy-proxy-protocol-and-tls-termination
category: computing-software
field: email-administration
product: dovecot
tags: [haproxy, proxy-protocol, send-proxy-v2, haproxy-trusted-networks, tls-termination, inet-listener-haproxy]
level: advanced
status: docs-checked
description: "Accept PROXY protocol v1 or v2 from HAProxy, trust only its addresses, and choose how TLS is terminated and forwarded."
sources:
  - https://doc.dovecot.org/main/core/config/proxy/haproxy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dovecot CE supports a single server only, so load balancing does not apply; the page documents the HAProxy-related features. HAProxy passes the real client IP with the PROXY protocol, and Dovecot accepts both v1 (text) and v2 (binary). Prefer v2, which can carry TLS metadata and parses less ambiguously. Dovecot uses the header to log the real address and apply IP-based restrictions.

HAProxy server-line directives:
- `send-proxy-v2`: client IP only.
- `send-proxy-v2-ssl`: adds TLS metadata (cipher, SNI) when HAProxy terminates TLS.
- `send-proxy-v2-ssl-cn`: also forwards the client certificate Common Name, which Dovecot treats as `cert_username` exactly as if it had terminated TLS.

Dovecot side: set `inet_listener_haproxy = yes` on the listener, and set `haproxy_trusted_networks` to a space-separated list of HAProxy addresses or CIDR ranges (for example 127.0.0.1 10.0.0.0/24). Clients from unlisted addresses connecting to a haproxy listener are rejected.

The recommended layout terminates client TLS at HAProxy and opens a new verified TLS connection to Dovecot (`ssl verify required`) while sending `send-proxy-v2-ssl`, so Dovecot logs the session as TLS. This protects the HAProxy-to-Dovecot path, centralizes certificate policy, and avoids exposing plaintext ports 143 and 110. Backend TLS adds nothing when both run on one host over 127.0.0.1. The same pattern applies to POP3, submission and ManageSieve.

## Checked

2026-11-03. Confirmed on the HAProxy page: Dovecot CE single-server note, PROXY v1 and v2 support with v2 preferred, send-proxy-v2, send-proxy-v2-ssl and send-proxy-v2-ssl-cn (cert_username), inet_listener haproxy = yes, haproxy_trusted_networks as a space-separated list with CIDR, rejection of unlisted clients, the recommended layout (ssl verify required plus send-proxy-v2-ssl, no plaintext 143/110), loopback needing no backend TLS, and the same pattern for POP3, submission and ManageSieve. Nothing removed.

Method: documentation only; no commands were run.
