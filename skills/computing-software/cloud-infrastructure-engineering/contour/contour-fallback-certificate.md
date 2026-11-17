---
id: computing-software.cloud-infrastructure-engineering.contour.contour-fallback-certificate
name: contour-fallback-certificate
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [fallback-certificate, enablefallbackcertificate, sni, legacy-clients, tlscertificatedelegation]
level: advanced
status: docs-checked
description: "Contour fallback certificate for TLS clients without SNI: config file secret, delegation, enableFallbackCertificate, and unsupported per-vhost policies."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/tls-termination.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fallback certificate for clients without SNI

Some legacy TLS clients do not send SNI, so Envoy cannot pick a certificate or vhost. A fallback certificate serves them.

Steps:
1. Name the Secret in the Contour config file under `tls.fallback-certificate` (`name`, `namespace`).
2. Delegate it to the namespaces allowed to use it with a TLSCertificateDelegation (`targetNamespaces` a list or `"*"`).
3. Opt in on each root HTTPProxy:

```yaml
spec:
  virtualhost:
    fqdn: fallback.bar.com
    tls:
      secretName: testsecret
      enableFallbackCertificate: true
  routes:
  - services: [{name: s1, port: 80}]
---
apiVersion: projectcontour.io/v1
kind: TLSCertificateDelegation
metadata:
  name: fallback-delegation
  namespace: www-admin
spec:
  delegations:
  - secretName: fallback-secret-name
    targetNamespaces: ["*"]
```

Constraints:
- The minimum TLS version for fallback requests is the `minimum-protocol-version` in the Contour config file.
- Fallback uses one shared connection manager for all participating vhosts, so per-vhost security policies are unsupported: TLS client authentication, external authorization and JWT verification cannot be combined with it.
- The HTTP Host header is encrypted in the handshake, so without SNI routing relies on decrypting with the default certificate first.

## Checked

2026-11-08: read the Contour docs config/tls-termination (Fallback Certificate section) and configuration (TLS and Fallback Certificate tables). Confirmed: no-SNI legacy clients, the fallback-certificate name and namespace fields in the config file, TLSCertificateDelegation to specific or all namespaces, enableFallbackCertificate on root HTTPProxy, the config-file minimum protocol version for fallback requests, the shared connection manager, and no per-vhost client auth, external authorization or JWT verification.

Method: documentation only; no commands were run.
