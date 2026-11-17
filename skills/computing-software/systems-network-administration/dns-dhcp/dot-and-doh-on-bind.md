---
id: computing-software.systems-network-administration.dns-dhcp.dot-and-doh-on-bind
name: dot-and-doh-on-bind
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, dns-over-tls, dns-over-https, dot, doh, encrypted-dns, tls-certificate, port-853, http-endpoint, kdig, named-conf]
level: advanced
status: docs-checked
description: "Serve encrypted DNS from BIND 9.18+: tls and http statements, listen-on with tls/http, certificates, DoT on 853 and DoH on 443, and testing with kdig and curl."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://datatracker.ietf.org/doc/html/rfc7858
  - https://datatracker.ietf.org/doc/html/rfc8484
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DoT and DoH on BIND

BIND can terminate DNS over TLS (RFC 7858, default port 853) and DNS over HTTPS (RFC 8484, default endpoint `/dns-query`, default port 443) natively. Zone transfers over TLS (XoT) use the same `tls` block.

## Configure
```
tls local-tls {
    cert-file "/etc/bind/tls/resolver.example.org.fullchain.pem";
    key-file  "/etc/bind/tls/resolver.example.org.key";
    protocols { TLSv1.2; TLSv1.3; };
    prefer-server-ciphers yes;
};
http local-http {
    endpoints { "/dns-query"; };
    listener-clients 1000;
    streams-per-connection 100;
};
options {
    listen-on port 53 { 10.0.0.53; };
    listen-on port 853 tls local-tls { 10.0.0.53; };                    // DoT
    listen-on port 443 tls local-tls http local-http { 10.0.0.53; };    // DoH
    listen-on-v6 port 853 tls local-tls { 2001:db8::53; };
    allow-recursion { internal; };
};
```
- Certificate: from your internal CA (clients must trust it) or a public CA for a public name; the name clients configure must match the certificate.
- `listen-on ... tls ephemeral` uses a key and certificate created for the running named process (testing only).
- An `http` listener requires `tls`; for an unencrypted listener behind a reverse proxy use `tls none` (`listen-on port 8080 tls none http local-http`) and let the proxy do TLS. Naming the `http` block `default` uses the default `/dns-query` endpoint.
- Key files must be readable by the user named runs as; the ARM warns TLS configuration may change incompatibly, so read release notes on upgrade.

## Test
```
dig +tls @10.0.0.53 +tls-hostname=resolver.example.org example.com
dig +https @10.0.0.53 +tls-hostname=resolver.example.org example.com
dig +https @resolver.example.org example.com
```

## Gotchas
- Port 443 conflicts with a web server on the same IP: use a dedicated IP.
- Firewalls must allow TCP 853 / 443 to the resolver (the defaults, overridable with `tls-port` and `https-port`).
- Encrypted transport protects the client-to-resolver hop only; the resolver still recurses in
  clear text upstream (unless forwarding over DoT).

## Verify
- [ ] dig over TLS and HTTPS returns answers and the certificate matches the configured name.
- [ ] Clients configured with the hostname validate the certificate (no fallback to plain DNS in strict mode).

## Checked

Date: 2026-10-26. BIND 9 ARM and man-page sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27; grammar cross-checked on bind-9.20), read on 2026-10-26. Confirmed: tls and http block grammar (cert-file, key-file, protocols, prefer-server-ciphers, endpoints, listener-clients, streams-per-connection), listen-on tls/http semantics (default ports 853/443/80 and 53, http requires tls, tls none, tls ephemeral, default endpoint /dns-query), dig +tls/+https/+tls-hostname options (dig man page). Removed kdig and the hand-built curl query (unconfirmed), and version gates.

Method: documentation only; no commands were run.
