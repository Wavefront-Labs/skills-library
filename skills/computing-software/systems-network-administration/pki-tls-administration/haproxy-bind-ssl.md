---
id: computing-software.systems-network-administration.pki-tls-administration.haproxy-bind-ssl
name: haproxy-bind-ssl
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [haproxy-bind-ssl, pki-haproxy, haproxy, bind-ssl, ssl-default-bind-options, crt, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Configure HAProxy TLS termination: crt files and directories, protocol floor, cipher lists, ALPN, OCSP auto-update and live certificate updates."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
  - https://docs.haproxy.org/3.0/management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HAProxy bind ssl options
Goal: TLS termination with explicit defaults. Checked against the HAProxy 3.0 manuals; other versions may differ.
```
global
  ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets
  ssl-default-bind-ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-GCM-SHA256
  ssl-default-bind-ciphersuites TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256
frontend fe
  bind :443 ssl crt /etc/haproxy/certs/ alpn h2,http/1.1
```
(The two cipher lines are the manual's own example.)
- `ssl-default-bind-ciphers` sets the cipher list for TLS 1.2 and earlier, in the format of OpenSSL `man 1 ciphers`. `ssl-default-bind-ciphersuites` sets the TLS 1.3 list (needs OpenSSL 1.1.1 or later); TLS 1.3 defines five suites, named with underscores such as `TLS_AES_128_GCM_SHA256`. Both apply only to `bind` lines that do not set their own.
- `ssl-min-ver` enforces that version or higher; its default is TLSv1.2, and it can be set in `ssl-default-bind-options`.
- `no-tls-tickets` disables stateless session resumption (RFC 5077 tickets) and forces stateful resumption. Tickets only apply up to TLS 1.2 and compromise forward secrecy unless ticket keys are rotated.
- `alpn`: needed to enable HTTP/2 on an HTTPS frontend. If none of `npn`, `alpn` or `no-alpn` is set, HAProxy uses `h2,http/1.1` on a regular HTTPS frontend. Protocols not advertised are not negotiated.
- `crt`: a PEM file may hold the certificate, private key and intermediates concatenated; with no key inside, HAProxy tries the same path suffixed `.key`. If a directory is given, every file in it loads in alphabetical order except names ending `.key`, `.issuer`, `.ocsp` or `.sctl`, and dot files. The certificate is picked by the client's SNI against CN or subject alternative names (wildcards cover one label only).
- Default certificate: with no SNI, an unsupported SNI, or no match, the first loaded certificate is presented, so load the intended default first. `strict-sni` refuses the handshake instead. An empty directory stops HAProxy starting unless `strict-sni` is used.
- OCSP: `ocsp-update on` (default `off`) can be set per crt-list line, for example `server_cert.pem [ocsp-update on] foo.bar`, in a crt-store, or globally with `tune.ocsp-update.mode`. Mixing different values for one certificate across crt-lists raises an error.
- Live updates: the runtime API `set ssl cert <filename> <payload>` starts a transaction and `commit ssl cert <filename>` applies it. The manual warns that an empty line ends the payload, so sanitise the PEM first.
- Config check: `haproxy -c -f <file>` only checks the configuration and exits non-zero on an error. Run it before a reload.

Verify:
- [ ] `haproxy -c -f /etc/haproxy/haproxy.cfg` exits zero.
- [ ] `openssl s_client -servername host -connect host:443` returns the expected certificate per host.

## Checked
Checked against the HAProxy 3.0 configuration manual (global ssl-default-bind-*, bind `crt`, `alpn`, `ssl-min-ver`, `no-tls-tickets`, `strict-sni`, `ocsp-update`) and management manual (`-c`, `set ssl cert`, `commit ssl cert`).
Corrected: TLS 1.3 suite names (the old text used `TLS_AES128_GCM_SHA256`, which is not a defined name).
Removed: the older cipher list (not in the manual), the `http-response set-header` HSTS line, the "2.8+" OCSP version note, the claim that a bad PEM aborts a reload, and the `systemctl reload` command (the manual describes reload by signal and init script only).
Method: docs-only read of cited pages, 2026-11-08
