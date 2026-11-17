---
id: computing-software.cryptography-implementation.key-management.cloud-hsm-services
name: cloud-hsm-services
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, aws-cloudhsm, cloud-hsm, azure-managed-hsm, pkcs11, fips-140-3-level-3]
level: advanced
status: draft
description: "Use dedicated cloud HSMs (AWS CloudHSM, Azure Cloud HSM and Managed HSM, Google Cloud HSM): cluster setup, crypto users, PKCS#11 clients, backups and when KMS suffices."
sources: ["https://docs.aws.amazon.com/cloudhsm/latest/userguide/introduction.html", "https://learn.microsoft.com/en-us/azure/key-vault/managed-hsm/overview", "https://cloud.google.com/kms/docs/hsm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud HSM services

## Which service
| Need | Service |
|---|---|
| Encrypt/decrypt/sign via API, managed keys | AWS KMS, Azure Key Vault, Google Cloud KMS (HSM protection level) |
| Single-tenant HSM, PKCS#11/JCE/KSP, own crypto users | AWS CloudHSM, Azure Cloud HSM (dedicated) |
| Single-tenant, Key Vault API, FIPS 140-3 Level 3 | Azure Managed HSM |
| HSM-backed keys via KMS API | Google Cloud HSM |

## AWS CloudHSM essentials
- Create a cluster in a VPC across at least two AZs (HSMs sync keys within the cluster).
- Initialize: sign the cluster CSR with your own CA, activate, create crypto users (CU) with `cloudhsm-cli`.
- Clients: PKCS#11 library, JCE provider, OpenSSL dynamic engine/provider, KSP/CNG.
- Backups are automatic, encrypted, and can be copied cross-region; you manage CU credentials, AWS cannot
  recover them.
- Key replication across HSMs in the cluster is automatic; verify key availability after adding HSMs.

## When to choose a dedicated HSM
- Regulatory need for sole control (PCI PIN, eIDAS QSCD-like, CA roots).
- Applications needing PKCS#11 or legacy HSM APIs.
- Otherwise KMS is cheaper and easier (no HA management, IAM integration, automatic rotation).

## Verify
- [ ] Cluster has at least 2 HSMs; restore from backup tested; CU credentials stored under dual control.
