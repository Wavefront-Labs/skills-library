---
id: computing-software.networking-hardware-and-wireless.traefik.tls-options-and-mtls
name: tls-options-and-mtls
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, tls-options, minversion, ciphersuites, clientauth, sni-strict, mtls]
level: practitioner
status: docs-checked
description: "Define Traefik TLS options for minimum version, ciphers and mutual TLS, and use core.strictTLSOptions to avoid silent fallback to default."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/tls/tls-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tls options and mtls
TLS options are named profiles referenced by `tls.options` on a router. Settings: `minVersion` (for example `VersionTLS12`), `cipherSuites`, `curvePreferences`, `sniStrict`, `alpnProtocols` and `clientAuth` with `caFiles` (`secretNames` on Kubernetes) and `clientAuthType`: NoClientCert, RequestClientCert, RequireAnyClientCert, VerifyClientCertIfGiven, RequireAndVerifyClientCert.

```yaml
tls:
  options:
    mtls:
      minVersion: VersionTLS12
      sniStrict: true
      clientAuth:
        caFiles:
          - /certs/clients-ca.pem
        clientAuthType: RequireAndVerifyClientCert
```
Gotcha: options are matched per hostname. If two routers on the same host and entrypoint (even from different providers) name different options, they conflict and Traefik falls back to `default`, where a router relying on `clientAuth` no longer enforces it. Set `core.strictTLSOptions: true` to fail closed: the conflicting routers are disabled instead.

## Checked
2026-11-03. Confirmed against the Traefik TLS options reference page: option names, the `default` option, per-hostname conflict detection across providers with fallback to `default`, and `core.strictTLSOptions` failing closed. Removed: the openssl handshake and log-warning Verify step.
Method: documentation only; no commands were run.


