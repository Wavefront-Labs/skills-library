---
id: computing-software.networking-hardware-and-wireless.haproxy.tls-termination-with-crt-lists
name: tls-termination-with-crt-lists
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, tls-termination, crt-list, ssl-min-ver, ciphersuites, sni-selection]
level: practitioner
status: docs-checked
description: "Terminate TLS in HAProxy with crt files, crt-list per-cert options, SNI selection and minimum protocol and cipher settings."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tls termination with crt lists
A PEM for `crt` holds the certificate chain then the private key (concatenated); a directory loads every file and serves the right one by SNI.

```
frontend fe_tls
    bind :443 ssl crt /etc/haproxy/certs/ crt-list /etc/haproxy/crt-list.txt alpn h2,http/1.1 ssl-min-ver TLSv1.2
```
`/etc/haproxy/crt-list.txt`:
```
/etc/haproxy/certs/site.pem [ocsp-update on alpn h2,http/1.1] example.com *.example.com
/etc/haproxy/certs/legacy.pem [ssl-min-ver TLSv1.0] legacy.example.com
```
Defaults: `global` can set `ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets`, `ssl-default-bind-ciphers` (TLS 1.2) and `ssl-default-bind-ciphersuites` (TLS 1.3). Use the Mozilla "intermediate" profile as a baseline. Certificate selection: an exact SNI match, then wildcard, then the first cert as default (the first loaded file); `strict-sni` refuses clients that send no matching SNI.

Gotchas: file order in a directory is alphabetical, and the default cert is the first one, so name it `00-default.pem`. ECDSA and RSA versions of one host are chosen by client capability if both are supplied as `site.pem.rsa` / `site.pem.ecdsa` bundles.

Verify: `openssl s_client -connect lb:443 -servername example.com </dev/null | openssl x509 -noout -subject -dates`; `testssl.sh lb:443` for protocol/cipher audit.

## Checked
2026-11-08: confirmed against the HAProxy 3.0 configuration manual (crt and crt-list, per-certificate options, ssl-min-ver, alpn, ocsp-update, strict-sni, ssl-default-bind-options, ssl-default-bind-ciphers and ssl-default-bind-ciphersuites, SNI selection, directory load order, .rsa and .ecdsa bundles). Removed: nothing.
Method: documentation only; no commands were run.
