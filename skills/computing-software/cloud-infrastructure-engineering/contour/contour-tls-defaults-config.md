---
id: computing-software.cloud-infrastructure-engineering.contour.contour-tls-defaults-config
name: contour-tls-defaults-config
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [tls-config, minimum-protocol-version, cipher-suites, ecdh-curves, fallback-certificate, envoy-client-certificate, ja3, ja4]
level: practitioner
status: docs-checked
description: "Contour config tls block: min/max protocol version, cipher suites, ECDH curves, fallback certificate, Envoy client certificate, JA3/JA4 fingerprinting, and upstream TLS defaults."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour tls block in the config file

Defaults for how Contour provisions TLS listeners:

```yaml
tls:
  minimum-protocol-version: "1.2"   # 1.2 default, 1.3 allowed
  maximum-protocol-version: "1.3"   # default 1.3
  cipher-suites:                     # TLS 1.2 ciphers
  - '[ECDHE-ECDSA-AES128-GCM-SHA256|ECDHE-ECDSA-CHACHA20-POLY1305]'
  - 'ECDHE-RSA-AES256-GCM-SHA384'
  ecdh-curves: [X25519, P-256]       # ordered by preference
  fallback-certificate:
    name: fallback-secret-name
    namespace: projectcontour
  envoy-client-certificate:
    name: envoy-client-cert-secret-name
    namespace: projectcontour
  fingerprint:
    ja3: true
    ja4: true
```

- Unknown protocol versions fall back to the default.
- `ecdh-curves`: when empty Envoy defaults (X25519, P-256) apply; when set, list the most preferred first.
- `fallback-certificate` serves requests whose SNI matches no vhost; each of `name`/`namespace` is a Secret reference.
- `envoy-client-certificate` is the Secret Envoy presents when connecting to TLS upstreams that require client auth.
- `fingerprint.ja3` / `ja4` (default false) compute TLS fingerprints on HTTPS listeners so they can be logged.

A parallel block `cluster.upstream-tls` has `minimum-protocol-version`, `maximum-protocol-version`, `cipher-suites` and `ecdh-curves` and sets defaults for upstream (Envoy to backend) TLS connections.

## Checked

2026-11-04. Confirmed against the Contour Configuration Reference (configuration.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
