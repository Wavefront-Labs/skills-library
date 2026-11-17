---
id: computing-software.systems-network-administration.headscale.server-url-listen-addr
name: server-url-listen-addr
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, server-url, listen-addr, metrics-listen-addr, trusted-proxies]
level: practitioner
status: docs-checked
description: "Set Headscale's server_url, listen_addr, metrics_listen_addr and trusted_proxies correctly, with the example-config defaults and spoofing warning."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/integration/reverse-proxy.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/tls.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/usage/getting-started.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Core address settings

From the example config:

```yaml
server_url: http://127.0.0.1:8080
listen_addr: 127.0.0.1:8080
metrics_listen_addr: 127.0.0.1:9090
trusted_proxies: []
disable_check_updates: false
```

- `server_url`: the URL clients connect to, typically a domain such as `https://myheadscale.example.com:443`.
- `listen_addr`: the address the server binds to. The config comment gives `0.0.0.0:8080` "for production".
- `metrics_listen_addr`: the address for `/metrics` and `/debug`; keep it private to your internal network. An empty value disables the metrics listener.
- `trusted_proxies`: CIDR(s) of reverse proxies whose True-Client-IP, X-Real-IP and X-Forwarded-For headers are honoured; empty (default) ignores those headers.
- `disable_check_updates`: disables the update check on startup.

## Gotchas

- `dns.base_domain` must differ from the `server_url` domain.
- Setting `trusted_proxies` without a proxy in front lets clients spoof their logged source IP.
- Behind a TLS-terminating reverse proxy the docs' base config uses `listen_addr: 127.0.0.1:8080` and empty `tls.cert_path` and `tls.key_path`; the startup warning "listening without TLS but ServerURL does not start with http://" is expected (reverse-proxy-requirements).
- With ACME, `tls.acme.hostname` must resolve to the address headscale is reachable on, i.e. correspond to `server_url`.

## Verify

`headscale configtest` validates the file; the health endpoint is `<server_url>/health`.

## Checked

2026-11-04. Confirmed against config-example.yaml (keys and defaults), the reverse proxy page (TLS warning, trusted proxies), the TLS page (ACME hostname) and the configuration and getting-started pages (configtest, health endpoint). Removed the unsourced advice to use a public domain in production.

Method: documentation only; no commands were run.
