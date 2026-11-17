---
id: computing-software.cryptography-implementation.protocol-implementation.tls-protocol-and-cipher-policy
name: tls-protocol-and-cipher-policy
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, tls-configuration, tls-server-config, tls-cipher-policy, rfc9325, bcp195, nginx, haproxy, apache]
level: practitioner
status: docs-checked
description: "Set a TLS server protocol and cipher policy from RFC 9325 (BCP 195): TLS 1.2+1.3 only, ECDHE+AEAD, per-server config snippets, and client-population checks."
sources: ["https://www.rfc-editor.org/rfc/rfc9325.txt", "https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://httpd.apache.org/docs/2.4/mod/mod_ssl.html", "https://docs.haproxy.org/3.0/configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS protocol and cipher policy

## Policy (RFC 9325 / BCP 195, 2022)

- MUST NOT negotiate SSLv2, SSLv3, TLS 1.0, TLS 1.1.
- SHOULD support TLS 1.3.
- TLS 1.2 recommended suites are the four ECDHE AES-GCM suites
  (`TLS_ECDHE_{RSA,ECDSA}_WITH_AES_{128,256}_GCM_SHA{256,384}`). CBC suites
  SHOULD NOT be used unless encrypt-then-MAC is negotiated.
- MUST NOT negotiate NULL or RC4 suites, or suites with less than 112 bits of
  security. SHOULD NOT negotiate static RSA
  key exchange (`TLS_RSA_WITH_*`) or static (non-ephemeral) DH/ECDH.
- Prefer forward secrecy. In TLS 1.2, SHOULD NOT negotiate finite-field DHE
  suites; if DH is used the key must be at least 2048 bits.
- TLS 1.2 implementations MUST support the `extended_master_secret` extension
  (RFC 7627) and the `renegotiation_info` extension (RFC 5746).
- Clients and servers SHOULD support the P-256 and X25519 curves.

ChaCha20-Poly1305 suites and extra curves (for example P-384) are widely
deployed but are not in RFC 9325's recommended list; add them only if your
client population needs them.

## Snippets

Directive names below are documented by nginx, Apache httpd and HAProxy; take
the cipher list itself from RFC 9325 section 4.2, not from old blog posts.

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ecdh_curve X25519:prime256v1;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_tickets off;     # unless ticket keys are rotated (see ticket skill)
```

```haproxy
global
  ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets
  ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:...
  ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384
```

```apache
SSLProtocol -all +TLSv1.2 +TLSv1.3
SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:...
SSLHonorCipherOrder off
SSLSessionTickets off
```

## Before tightening, look at real clients

- Log negotiated protocol and cipher (`$ssl_protocol $ssl_cipher` in nginx log
  format) for a week; check who still uses TLS 1.0/1.1 or CBC suites.
- Internal clients (old Java, embedded devices, payment terminals) are the
  usual blockers; upgrade or front them with a separate legacy listener that
  is monitored and time-limited.

## Verify

- [ ] A TLS scanner against the endpoint shows only TLS 1.2/1.3 and AEAD suites.
- [ ] Access logs show negotiated versions; legacy clients have a migration plan.

## Checked

2026-10-31. Confirmed in RFC 9325: MUST NOT for SSLv2/v3/TLS 1.0/1.1, SHOULD support TLS 1.3, the four recommended TLS 1.2
suites, CBC only with encrypt-then-MAC, MUST NOT for NULL/RC4/sub-112-bit suites, SHOULD NOT for static RSA and static
DH/ECDH, DHE SHOULD NOT in TLS 1.2 and 2048-bit minimum, `extended_master_secret` and `renegotiation_info` MUST, P-256
and X25519 SHOULD. Directive names (`ssl_protocols`, `ssl_ecdh_curve`, `ssl_ciphers`, `ssl_prefer_server_ciphers`,
`ssl_session_tickets`, `$ssl_protocol`/`$ssl_cipher`, `SSLProtocol`, `SSLCipherSuite`, `SSLHonorCipherOrder`,
`SSLSessionTickets`, HAProxy `ssl-default-bind-*`, `ssl-min-ver`, `no-tls-tickets`) were found in the nginx, Apache
mod_ssl and HAProxy 3.0 pages. Removed: Mozilla "intermediate/modern" profile claims and client versions (wiki page is a
script stub), ChaCha20 and P-384 as policy, `ssl_session_timeout` value, named scanner commands, RFC-attributed claims
that RFC 9325 does not make.
Method: documentation only; no commands were run.
