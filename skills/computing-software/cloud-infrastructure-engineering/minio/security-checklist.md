---
id: computing-software.cloud-infrastructure-engineering.minio.security-checklist
name: security-checklist
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, security-checklist, firewall, port-9000, port-9090, encryption-at-rest, encryption-in-transit, kes, kms-providers]
level: practitioner
status: docs-checked
description: "Walk the MinIO production security checklist from IAM policies and firewall ports 9000 and 9090 to KES encryption at rest and TLS in transit."
sources: ["https://github.com/minio/docs/blob/main/source/operations/checklists/security.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO security checklist

## Required steps
- Define group policies and individual access policies, on MinIO or on the external identity provider (LDAP/Active Directory or OpenID).
- Kubernetes only: configure each tenant for the chosen identity provider.
- Open TCP to the S3 API listen port (default `9000`) and the Console port (recommended default `9090`).

## Encryption at rest
KES (Key Encryption Service) fronts the external KMS. Supported root KMS providers: HashiCorp Vault, AWS, Google Cloud Platform Secret Manager and Azure Key Vault. Checklist order:
1. Download and install KES.
2. Enable TLS.
3. Generate keys and certificates for KES and for MinIO.
4. Create the KES configuration file and start the service.
5. Create an external key in the KMS.
6. Connect MinIO to KES.
7. Enable server-side encryption.

See `computing-software.cloud-infrastructure-engineering.minio.kes-configuration` and `computing-software.cloud-infrastructure-engineering.minio.sse-kms`.

## Encryption in transit
- Enable TLS.
- Provide separate certificates and keys for each internal and external domain that reaches MinIO.
- Use supported ciphers for TLS 1.3 or 1.2.
- Configure trusted CA stores.
- Expose the Kubernetes service, for example with NGINX.
- Optionally validate certificates.

See `computing-software.cloud-infrastructure-engineering.minio.enable-tls`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Security Checklist page (security.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
