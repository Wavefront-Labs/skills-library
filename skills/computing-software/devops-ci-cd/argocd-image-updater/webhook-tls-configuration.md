---
id: computing-software.devops-ci-cd.argocd-image-updater.webhook-tls-configuration
name: webhook-tls-configuration
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, webhook, tls, disable-tls, tls-min-version, tls-ciphers, argocd-image-updater-tls, http2]
level: advanced
status: docs-checked
description: "Configure webhook TLS: TLS 1.3 by default, own certificate via argocd-image-updater-tls, paths, versions, ciphers, curves, or disable TLS."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/webhook.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/webhook.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/run.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Webhook TLS configuration

The webhook server runs HTTPS with TLS 1.3 by default. It loads `tls.crt` and `tls.key` from the `argocd-image-updater-tls` Secret mounted at `/app/config/webhook/tls/`. If missing or empty it generates an in-memory self-signed certificate, which verifying senders will reject; check the log for a warning naming the missing file.

Own certificate: a Secret of type `kubernetes.io/tls` named `argocd-image-updater-tls` with `tls.crt` and `tls.key`. Other locations: `--tls-cert-path` / `--tls-key-path` (env `TLS_CERT_PATH`, `TLS_KEY_PATH`) set both. The old default `/app/config/tls/` is still read, with a deprecation warning, only when the defaults are in use; that directory now holds the `argocd-tls-certs-cm` trust store.

Plain HTTP: `--disable-tls` or `DISABLE_TLS=true`. HTTP/2 is off by default: `--enable-http2`.

Versions, ciphers, curves:

```bash
argocd-image-updater webhook --tlsminversion 1.2 --tlsmaxversion 1.3
argocd-image-updater webhook --tlsminversion 1.2 \
  --tlsciphers TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384:TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
argocd-image-updater webhook --tlscurvepreferences X25519MLKEM768:X25519:CurveP256
```

- min and max default `1.3`; valid `1.1`, `1.2`, `1.3`; a min of `1.0` is clamped to `1.2` with a warning; a max of `1.0` is an error
- `--tlsciphers` affects only TLS 1.2 and lower; TLS 1.3 suites are not configurable
- curves are an allow-list, order ignored; hybrid post-quantum groups are TLS 1.3 only, so include `X25519` or `CurveP256` for older clients

ConfigMap keys: `disable-tls`, `tls.cert-path`, `tls.key-path`, `tls.min-version`, `tls.max-version`, `tls.ciphers`, `tls.curve-preferences`.

## Checked

2026-11-08. Read in full: docs/configuration/webhook.md, docs/install/cmd/webhook.md and docs/install/cmd/run.md. Confirmed the TLS defaults, certificate paths and the deprecated fallback path, version, cipher and curve rules, the --disable-tls and --enable-http2 flags and the ConfigMap keys. Nothing removed.

Method: documentation only; no commands were run.
