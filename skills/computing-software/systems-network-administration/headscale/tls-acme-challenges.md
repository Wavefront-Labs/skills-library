---
id: computing-software.systems-network-administration.headscale.tls-acme-challenges
name: tls-acme-challenges
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, acme, http-01, tls-alpn-01, dns-01, lets-encrypt]
level: advanced
status: docs-checked
description: "Let Headscale obtain Let's Encrypt certificates: tls.acme settings, HTTP-01 versus TLS-ALPN-01 versus DNS-01, and the port 80 and 443 conflicts."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/tls.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Let's Encrypt (ACME)

```yaml
tls:
  acme:
    hostname: ""
    http_listen: ":http"
    cache_dir: /var/lib/headscale/cache
    challenge_type: HTTP-01
```

- `hostname` must resolve to Headscale's IP address(es) and match `server_url`.
- `cache_dir` stores the certificate and account credentials.
- `challenge_type`: `HTTP-01` (default), `TLS-ALPN-01` or `DNS-01`; `dns.challenge.provider` selects the DNS provider for DNS-01.
- Other keys in the example config: `acme.url` (ACME directory) and `acme.email`.

## HTTP-01

Headscale must be reachable on port 80 as well as `listen_addr`. `listen_addr` and `tls.acme.http_listen` cannot bind the same socket; use `listen_addr` on 443 (e.g. `0.0.0.0:443`), not `0.0.0.0:80`. Otherwise startup fails with `listen_addr and tls.acme.http_listen would bind the same TCP socket` or `address already in use`.

Let's Encrypt only connects to port 80, so if you change `http_listen`, forward port 80 to it (useful when running as non-root without `setcap`).

## TLS-ALPN-01

Headscale listens on `listen_addr`; Let's Encrypt only connects to 443, so forward 443 to it if you use another port.

## Debug

CertMagic log lines are marked `logger=acme`.

## Checked

2026-11-04. Confirmed against the Headscale TLS reference and config-example.yaml: the tls.acme block and defaults, three challenge types, `dns.challenge.provider`, `acme.url` and `acme.email`, the listen_addr versus http_listen conflict and its startup message, port 80 and 443 forwarding, and `logger=acme`.
Method: documentation only; no commands were run.
