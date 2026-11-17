---
id: computing-software.networking-hardware-and-wireless.haproxy.sni-routing-tls-passthrough
name: sni-routing-tls-passthrough
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, ssl-passthrough, req-ssl-sni, sni-routing, tcp-request-inspect-delay]
level: practitioner
status: docs-checked
description: "Route TLS connections by SNI in HAProxy without decrypting, using tcp-request inspect-delay and req.ssl_sni, with send-proxy-v2 to pass client IP."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sni routing tls passthrough
For end-to-end TLS in TCP mode, HAProxy waits for the ClientHello and picks a backend from the requested server name without decrypting.

```
frontend fe_tls
    bind :443
    mode tcp
    tcp-request inspect-delay 5s
    tcp-request content accept if { req.ssl_hello_type 1 }
    use_backend be_a if { req.ssl_sni -i a.example.com }
    use_backend be_b if { req.ssl_sni -m end .b.example.com }
    default_backend be_default
backend be_a
    mode tcp
    server a 10.0.0.11:443 check send-proxy-v2
```
- `tcp-request inspect-delay <timeout>` withholds data for up to that time so content rules can see it. Rules are re-evaluated on every new chunk; if none matches before the delay ends, a last check treats the contents as definitive. With no delay set HAProxy does not wait at all, which the manual calls unlikely to be useful and possibly racy.
- Content switching on SNI: wait for a complete client hello (`req.ssl_hello_type 1`) first, as in the manual's example.
- `req.ssl_sni` returns the Server Name extension from the raw request buffer. It does not work on `bind` lines with `ssl` (use `ssl_fc_sni` there). It only works for implicit-TLS protocols such as HTTPS (443), IMAPS (993) and SMTPS (465), not for explicit-TLS protocols such as SMTP (25/587) or IMAP (143).
- `req.ssl_alpn` returns the client's ALPN list from the ClientHello, usable the same way, for example `use_backend bk_acme if { req.ssl_alpn acme-tls/1 }`.
- Match flags: `-i` ignores case, `-m end` is a suffix match; `-f <file>` loads a list of allowed names, as in the manual example.
- `send-proxy-v2` on the server line sends PROXY protocol v2 so the server learns the client's layer 3/4 addresses (and ALPN if one was negotiated); only use it when the server understands that version. `send-proxy-v2-ssl` and `proxy-v2-options` add TLS details.

Limits stated by the manual: only the first ClientHello is parsed, so a TLS 1.3 HelloRetryRequest or a renegotiation carrying a different SNI is ignored. With Encrypted Client Hello, `req.ssl_sni` returns the decoy SNI of the outer ClientHello and must not be used for routing or access control. The value is not reliable enough to allow or deny access to hosts on its own.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual: `tcp-request inspect-delay`, the `req.ssl_sni`, `req.ssl_alpn` and `req.ssl_hello_type` fetches (including the HelloRetryRequest, renegotiation and ECH limitations), `send-proxy-v2`, `proxy-v2-options`, and the `-i`/`-m end` match flags. Removed: the mixed-mode "SNI split" via an `abns@loopback` bind with `accept-proxy` (not described as a pattern in the manual), the claim that `req.ssl_sni` is empty without `inspect-delay`, the `check` keyword semantics for passthrough, and the `openssl s_client` verification. Read as sections of the manual only.
Method: documentation only; no commands were run.
