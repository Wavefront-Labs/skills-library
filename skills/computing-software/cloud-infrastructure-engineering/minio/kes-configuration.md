---
id: computing-software.cloud-infrastructure-engineering.minio.kes-configuration
name: kes-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, kes-configuration, key-encryption-service, kes, sealed-vault, kms-target, mc-admin-service-restart, tenant-encryption]
level: advanced
status: docs-checked
description: "Deploy MinIO with KES for production SSE: prerequisites, supported KMS targets, the sealed Vault failure mode, Kubernetes tenant settings and procedure order."
sources: ["https://github.com/minio/docs/blob/main/source/operations/server-side-encryption/configure-minio-kes.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure MinIO with KES for server-side encryption

Procedure for production SSE with KES and a supported KMS. Assumes a production KMS, one or more KES servers connected to it, and hosts for a new or existing MinIO deployment.

## Kubernetes flow
1. Create or modify a MinIO tenant (with the Operator).
2. In the Operator Console, open the tenant's **Encryption** settings and configure SSE with a supported KMS.
3. Create a new External Key (EK).
4. Configure automatic bucket-default SSE-KMS.
Prerequisites: kubectl admin rights over pods, statefulsets, replicasets, deployments and secrets; a KMS reachable from the cluster (in-cluster you can use Kubernetes service names; external KMS needs routing from pods to the external network).

## Baremetal flow
1. Create an EK.
2. Create or modify the deployment with KES support (see the distributed deployment tutorial).
3. Configure automatic bucket-default SSE-KMS.
Prerequisites: `mc` with a configured alias, and an existing KES installation connected to a supported KMS, both reachable from the host.

## Supported KMS targets
AWS Secrets Manager, Azure KeyVault, Entrust KeyControl, Fortanix SDKMS, Google Cloud Secret Manager, HashiCorp Vault, Thales CipherTrust Manager. Follow the KES documentation for your target.

## Sealed KMS gotcha
KES operations need an unsealed target. If the KMS (for example Vault) is sealed or restarted, KES errors and no cryptographic operation succeeds until it is unsealed. Check your KMS docs on whether unsealing is required.

Key-level background: `computing-software.cloud-infrastructure-engineering.minio.sse-overview`; checklist order: `computing-software.cloud-infrastructure-engineering.minio.security-checklist`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Server-Side Object Encryption with KES page (configure-minio-kes.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
