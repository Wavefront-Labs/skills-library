---
id: computing-software.cryptography-implementation.key-management.maintaining-a-key-inventory
name: maintaining-a-key-inventory
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, key-inventory-register, key-inventory, sp-800-57, pci-dss, key-metadata, cryptographic-inventory, asset-management]
level: practitioner
status: draft
description: "Build and keep a cryptographic key inventory register: required fields per SP 800-57 and PCI DSS, discovery sources, ownership, and reconciliation cadence."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt2/r1/final", "https://csrc.nist.gov/pubs/sp/800/130/final", "https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Maintaining a key inventory

You cannot rotate, revoke or destroy keys you do not know about. PCI DSS 4.0 (3.6.1.1 for service providers, 12.3.3
for cipher suites) and SP 800-57 Part 2 both expect a maintained inventory.

## Fields per key (register row)
| Field | Example |
|---|---|
| Key ID / alias / version | `alias/payments-dek`, v7 |
| Type and purpose (SP 800-57 key type) | Symmetric data-encryption key |
| Algorithm, size, mode | AES-256-GCM |
| Location and protection | AWS KMS, HSM-backed, us-east-1 |
| Owner and custodians | Payments team; 2 named custodians |
| Systems and data protected | `orders` DB column `card_token` |
| Created, activation, cryptoperiod, next rotation | 2026-03-01, 1 year |
| State | Active / Suspended / Deactivated / Compromised / Destroyed |
| Backup / escrow location | KMS multi-region replica |
| Compliance scope | PCI, SOX |

Certificates and their private keys belong in the same register (or a linked certificate inventory).

## Discovery sources
- KMS/HSM APIs: `aws kms list-keys` + `describe-key`, `gcloud kms keys list`, `az keyvault key list`,
  `pkcs11-tool --list-objects`.
- Secrets managers: Vault mounts and KV paths, AWS Secrets Manager `list-secrets`.
- Code and config scans for embedded keys (gitleaks, trufflehog) and keystores (`*.jks`, `*.p12`, `*.pem`).
- Network scans for TLS certificates; CT logs for your domains.
- Cloud asset inventory (AWS Config, Azure Resource Graph, GCP Asset Inventory).

## Keeping it true
- Reconcile monthly: discovered minus registered = unknown keys to triage; registered minus discovered = deleted or
  drifted.
- Create entries automatically from infrastructure-as-code (tags/labels on KMS keys: owner, purpose, data class).
- Every key without an owner is escalated, not ignored.

## Verify
- [ ] Reconciliation report has zero unowned keys.
- [ ] Every PCI-scope key shows cryptoperiod and next rotation date.
