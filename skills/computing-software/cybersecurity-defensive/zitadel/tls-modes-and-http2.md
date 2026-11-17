---
id: computing-software.cybersecurity-defensive.zitadel.tls-modes-and-http2
name: tls-modes-and-http2
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, tls, http2, h2c, grpc, reverse-proxy]
level: advanced
status: docs-checked
description: "Choose between the disabled, external and enabled TLS modes and keep HTTP/2 working end to end for gRPC."
sources:
  - https://zitadel.com/docs/self-hosting/manage/tls_modes
  - https://zitadel.com/docs/self-hosting/manage/http2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL has three TLS modes, set with `--tlsMode`:

```bash
zitadel start-from-init --masterkey "MasterkeyNeedsToHave32Characters" --tlsMode disabled
```

- `disabled`: plain HTTP without TLS; not secure, for test systems only.
- `external`: ZITADEL tells clients to use https but a reverse proxy, web application firewall or service mesh manages TLS.
- `enabled`: ZITADEL itself accepts encrypted connections. Configure `TLS.Enabled: true` plus a private key and certificate, either as paths (`KeyPath`, `CertPath`) or as base64 values (`Key`, `Cert`). Paths override inline values.

HTTP/2 is essential. ZITADEL's APIs use gRPC, also offered as REST and gRPC-web for browsers. By default HTTP/2 is encrypted. If a proxy or mesh talks to ZITADEL without TLS, use h2c, unencrypted HTTP/2. This is common in service meshes and serverless platforms such as Google Cloud Run or Knative.

Therefore in `external` or `disabled` mode, verify h2c compatibility of your proxy or mesh. gRPC requires HTTP/2 between the application and ZITADEL.

## Checked

2026-11-08. Read the TLS modes and HTTP/2 pages in full; removed an unsupported claim that external is most common and an unsupported HTTP/1.1 statement.

Method: documentation only; no commands were run.
