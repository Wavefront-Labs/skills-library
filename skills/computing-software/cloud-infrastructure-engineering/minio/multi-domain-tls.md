---
id: computing-software.cloud-infrastructure-engineering.minio.multi-domain-tls
name: multi-domain-tls
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, multi-domain-tls, sni, server-name-indication, subject-alternate-name, default-certificate, tls-san]
level: advanced
status: docs-checked
description: "Serve several hostnames from one MinIO deployment with SNI, where MinIO picks the certificate by SAN match and falls back to the default certificate."
sources: ["https://github.com/minio/docs/blob/main/source/operations/network-encryption/enable-multiple-domain-minio-tls.rst", "https://github.com/minio/docs/blob/main/source/operations/network-encryption.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO multiple-domain TLS (SNI)

MinIO supports Server Name Indication: when a client connects with a hostname, MinIO looks for the TLS certificate that covers it.

## Rules
- At minimum one **default** certificate is required; more can be added for SNI.
- MinIO uses the certificate Subject Alternate Name (SAN) list to choose. If no certificate SAN covers the requested hostname, MinIO falls back to the default certificate and attempts the handshake. That is the least configuration but exposes every hostname in the default certificate's SAN to connecting clients.
- Baremetal: the server detects certificates in its certs directory and enables TLS on discovery (`computing-software.cloud-infrastructure-engineering.minio.enable-tls`).
- Kubernetes: the Operator accepts user-specified certificates when you deploy or modify a tenant. Certificates signed by your organisation's CA work as long as applications trust that CA.

## Kubernetes trust notes
- Pods get a CA bundle at `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt`, which should include the cluster or root CA that signed tenant certificates. In-cluster apps can reach a tenant through its service DNS name, for example `https://minio.minio-tenant-1.svc.cluster-domain.example:443`.
- Secrets supplied for TLS may be `opaque` or `kubernetes.io/tls` and must contain `private.key` and `public.crt`.
- For tenants using certificates from a private CA, or a public CA with intermediates, give the Operator the CA: `kubectl create secret generic operator-ca-tls --from-file=public.crt -n minio-operator`, then restart the Operator. One file can hold several CAs if BEGIN and END delimiters are kept. CA changes on a tenant take effect after a tenant restart.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Enable Multiple Domain TLS page (enable-multiple-domain-minio-tls.rst) and the Network Encryption page (network-encryption.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
