---
id: computing-software.cloud-infrastructure-engineering.minio.enable-tls
name: enable-tls
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, enable-tls, tls, certs-dir, private-key, public-crt, certgen, self-signed, tls-1-2]
level: practitioner
status: docs-checked
description: "Enable TLS on MinIO baremetal by placing private.key and public.crt in the default or --certs-dir directory, generate test certs with certgen, and enable tenant TLS on Kubernetes."
sources: ["https://github.com/minio/docs/blob/main/source/operations/network-encryption/enable-minio-tls.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable TLS for MinIO

MinIO supports TLS 1.2+ for incoming and outgoing traffic. Use certificates with a supported cipher suite.

## Baremetal
MinIO searches each node for certificates and **automatically enables TLS** when it finds and validates them.
- Default directory: `${HOME}/.minio/certs` of the user running MinIO (create it if absent; for `systemd` it must match the service `USER`; if that user has no home, use a custom path).
- Custom directory: `minio server --certs-dir /opt/minio/certs ...` (or `-S`). The service user needs read and write permission.
- Files for the default domain: `private.key` and `public.crt`.
- Self-signed for evaluation: `certgen -host "localhost,minio-*.example.net"` (MinIO certgen) or `openssl`. For production use your internal CA or a public CA.

## Kubernetes (Operator)
Three methods, combinable: MinIO auto-TLS, cert-manager, user-managed secrets. cert-manager is strongly recommended for renewal. Edit the Tenant spec (Kustomize):
- Auto-TLS: `requestAutoCert: true` plus `certConfig` with `commonName`, `organizationName` and `dnsNames`.
- cert-manager: `requestAutoCert: false` and `externalCertSecret` entry `{name: myminio-tls, type: cert-manager.io/v1}`.
- User-managed: `requestAutoCert: false` and `externalCertSecret` entry with `type: kubernetes.io/tls`.
Applying the new template makes the Operator redeploy the tenant. Tenants can also run without TLS.

SSE and many other features require TLS (`computing-software.cloud-infrastructure-engineering.minio.sse-overview`). Multiple hostnames: `computing-software.cloud-infrastructure-engineering.minio.multi-domain-tls`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Enable TLS for MinIO page (enable-minio-tls.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
