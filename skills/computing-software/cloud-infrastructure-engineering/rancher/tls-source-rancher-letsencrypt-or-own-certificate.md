---
id: computing-software.cloud-infrastructure-engineering.rancher.tls-source-rancher-letsencrypt-or-own-certificate
name: tls-source-rancher-letsencrypt-or-own-certificate
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [tls, cert-manager, letsencrypt, ingress-tls-source, privateca, certificates]
level: practitioner
status: docs-checked
description: "Choose among the three Rancher Helm TLS sources: rancher-generated CA, Let's Encrypt via HTTP-01, or your own secret, with the matching chart flags and cert-manager requirement."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/install-upgrade-on-a-kubernetes-cluster
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ingress.tls.source` selects where the ingress certificate comes from. The three documented values map to three install commands.

| Source | Chart option | cert-manager |
|---|---|---|
| Rancher-generated (default) | `ingress.tls.source=rancher` | required |
| Let's Encrypt | `ingress.tls.source=letsEncrypt` | required |
| Certificates from files | `ingress.tls.source=secret` | not needed |

**Rancher-generated:** Rancher makes its own CA and cert-manager issues and maintains a certificate from it. Nothing extra is needed unless `agent-tls-mode` is `strict`, covered separately.

**Let's Encrypt:** uses HTTP-01 validation, so the load balancer needs a public DNS record, be reachable from the internet, and port 80 must be open. Set `letsEncrypt.email` and `letsEncrypt.ingress.class` (traefik, nginx, haproxy and so on). With `agent-tls-mode` strict (the default for new installs from v2.9.0) you must also set `privateCA=true` and upload the Let's Encrypt CA, otherwise Rancher may fail to connect to downstream clusters.

**Own certificate:** `hostname` must match the certificate's Common Name or a Subject Alternative Name, or the ingress fails to configure. Install with `ingress.tls.source=secret`, add `--set privateCA=true` for a private CA, then publish the files as secrets. The private CA certificate is needed because nodes may not trust it, and Rancher derives a checksum from it that components use to validate their connection.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Install/Upgrade Rancher on a Kubernetes Cluster. Nothing removed.

Method: documentation only; no commands were run.
