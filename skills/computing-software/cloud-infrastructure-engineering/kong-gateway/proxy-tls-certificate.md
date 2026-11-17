---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.proxy-tls-certificate
name: proxy-tls-certificate
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, ssl-cert, admin-ssl-cert, client-ssl, tls, kong-conf, mtls]
level: practitioner
status: docs-checked
description: "Default TLS certificates in kong.conf: ssl_cert/ssl_cert_key for the proxy, admin_ssl_cert for the Admin API, and client_ssl for mTLS to upstreams."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
  - https://developer.konghq.com/gateway/entities/sni/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxy and Admin API TLS certificates

| Setting | Default | Purpose |
|---|---|---|
| `ssl_cert` / `ssl_cert_key` | empty | certificate and key for the proxy TLS listener |
| `admin_ssl_cert` / `admin_ssl_cert_key` | empty | certificate and key for the Admin API TLS listener |
| `client_ssl` | `off` | send a client certificate to upstreams (mTLS) |
| `client_ssl_cert` / `client_ssl_cert_key` | empty | the client certificate and key used when `client_ssl` is on |

If `ssl_cert` is unset, Kong auto-generates RSA and ECC default certificates on first start and uses them as the fallback.

Per-hostname certificates are normally managed as Certificate and SNI entities through the Admin API; the file-based `ssl_cert` is the default served when no SNI matches (the last step of SNI resolution is the default certificate on the file system).

Certificates and keys may be given as an absolute path, the content, or base64-encoded content.

For per-Service upstream client certificates use the Service `client_certificate` field instead of the global `client_ssl_cert`.

## Checked

2026-11-04. Confirmed against kong.conf.default (`ssl_cert`, `admin_ssl_cert`, `client_ssl` and `client_ssl_cert` settings and defaults, auto-generated RSA and ECC certificates, accepted value forms, the Service `client_certificate` override) and the SNI entity page (default certificate on the file system as the last resolution step). Replaced the vault-reference sentence, which the page does not state for these settings.
Method: documentation only; no commands were run.
