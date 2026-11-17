---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-tls-options
name: telegraf-tls-options
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [tls, mutual-tls, certificates, tls-ca, insecure-skip-verify]
level: practitioner
status: docs-checked
description: "Lists the standard Telegraf TLS client and server settings, mutual TLS options and version and cipher controls. Use when securing plugin connections."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/tls/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Standard TLS options

Plugins that support TLS use the same settings. Client settings appear on plugins that connect out; server settings on plugins that listen.

## Client

```toml
[[inputs.http]]
  urls = ["https://server.company.org/metrics"]
  tls_ca = "/etc/telegraf/ca.pem"
  tls_cert = "/etc/telegraf/cert.pem"
  tls_key = "/etc/telegraf/key.pem"
```

- `tls_enable`: force TLS on or off. Unset means TLS is enabled if any other TLS option is set.
- `tls_ca`: PEM root certificates to verify the server; default is the system pool.
- `tls_cert` / `tls_key`: PEM certificate (may include intermediates) and its key.
- `tls_key_pwd`: passphrase for an encrypted PKCS#8 key. Encrypted PKCS#1 keys are not supported.
- `insecure_skip_verify`: skip chain and host name verification, default false. Testing only; it permits machine-in-the-middle attacks.
- `tls_server_name`: SNI server name to send.

## Server

Listening plugins add `tls_allowed_cacerts` (setting it enables mutual TLS; client certificates must be signed by one of the CAs) and `tls_allowed_dns_names` (any matching SAN is accepted).

## Advanced

`tls_cipher_suites` (default: Go's defaults), `tls_min_version` (default `TLS12`) and `tls_max_version`.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): TLS configuration page: client, server and advanced options, defaults and key-format notes. Removed: nothing.

Method: documentation only; no commands were run.
