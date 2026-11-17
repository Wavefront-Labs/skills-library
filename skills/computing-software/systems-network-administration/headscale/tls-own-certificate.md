---
id: computing-software.systems-network-administration.headscale.tls-own-certificate
name: tls-own-certificate
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, tls, cert-path, key-path, full-chain]
level: practitioner
status: docs-checked
description: "Serve Headscale over TLS with your own certificate: cert_path and key_path, full chain requirement, relative paths, and keep-old-cert failure behaviour."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/tls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bring your own certificate

```yaml
tls:
  cert_path: ""
  key_path: ""
```

- `cert_path`: certificate file; use the full chain.
- `key_path`: key file.
- Relative `cert_path`, `key_path` and `cache_dir` paths resolve from the config file's directory.

## Gotchas

- Use the full chain: some clients, such as the Tailscale Android client, reject the certificate otherwise.
- Reload with SIGHUP to pick up a renewed certificate (tls-reload-renewal). If files fail to load, or the certificate is expired or not yet valid, Headscale logs an error and keeps the previous certificate.
- Behind a reverse proxy the reverse-proxy page leaves these empty and lets the proxy handle TLS (reverse-proxy-requirements).

## Check expiry

Open the server URL in a browser, or:

```
openssl s_client -servername [hostname] -connect [hostname]:443 | openssl x509 -noout -dates
```

## Verify reload

After `sudo systemctl reload headscale`, the log line `TLS certificate reloaded` confirms success. New connections get the new certificate; open connections keep the old one.

## Checked

2026-11-04. Confirmed against the Headscale TLS and reverse-proxy pages: cert_path and key_path, full chain and the Android client remark, relative paths, SIGHUP reload, keep-old-certificate behaviour, `TLS certificate reloaded`, and the openssl expiry check.
Method: documentation only; no commands were run.
