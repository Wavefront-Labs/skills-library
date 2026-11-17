---
id: computing-software.systems-network-administration.pki-tls-administration.haproxy-crt-list
name: haproxy-crt-list
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [haproxy-crt-list, pki-haproxy, haproxy, crt-list, sni-filter, runtime-api, pki-tls-administration]
level: practitioner
status: draft
description: "Use crt-list for per-certificate options, SNI filters and ALPN, and hot-swap certificates through the runtime API."
sources:
  - https://docs.haproxy.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HAProxy crt-list and SNI filters
Goal: per-site TLS settings and zero-downtime renewals.
`/etc/haproxy/crt-list.txt`:
```
/etc/haproxy/certs/a.pem [ocsp-update on alpn h2,http/1.1] a.example.com
/etc/haproxy/certs/b.pem [ssl-min-ver TLSv1.3] b.example.com *.b.example.com
/etc/haproxy/certs/default.pem
```
`bind :443 ssl crt-list /etc/haproxy/crt-list.txt`
- Hot update after renewal:
```
echo -e "set ssl cert /etc/haproxy/certs/a.pem <<\n$(cat new.pem)\n" | socat stdio /var/run/haproxy.sock
echo "commit ssl cert /etc/haproxy/certs/a.pem" | socat stdio /var/run/haproxy.sock
```
- Optionally enable `strict-sni` so unknown SNI fails instead of using the first cert.
- Combine fullchain and key in deploy hooks (`cat fullchain privkey`).
Gotcha: the runtime API changes memory only; update the file on disk too or the next reload reverts.
Verify:
- [ ] `show ssl cert /etc/haproxy/certs/a.pem` shows the new expiry.
- [ ] No handshake errors in logs after commit.
