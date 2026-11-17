---
id: computing-software.cryptography-implementation.key-management.dual-control-and-split-knowledge
name: dual-control-and-split-knowledge
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-management-policy, dual-control, split-knowledge, separation-of-duties, pci-dss, multi-party-approval, quorum-authentication, key-components]
level: advanced
status: gated
description: "Implement dual control and split knowledge for sensitive key operations: key components with XOR and KCV, HSM quorum auth, KMS multi-party approval, and separating admin from use."
sources: ["https://www.pcisecuritystandards.org/document_library/", "https://csrc.nist.gov/pubs/sp/800/57/pt2/r1/final", "https://docs.aws.amazon.com/cloudhsm/latest/userguide/quorum-authentication.html", "https://www.x9.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dual control and split knowledge

PCI DSS (the key-management requirements in section 3; confirm the exact requirement numbers in the current version, e.g. 3.7.6 for manual cleartext key operations in v4.0 (gated: unconfirmed, source is paywalled or blocked)) and payment HSM practice (ANSI X9.24, PCI PIN)
require that no single person can know or use a whole cleartext key or
perform critical key operations alone.

- **Split knowledge**: the key exists only as components; each custodian
  knows one.
- **Dual control**: two or more people must act together for the operation.
- **Separation of duties**: those who administer keys cannot use them for
  data access, and vice versa.

## Key components (classic method)

A 256-bit key K = C1 XOR C2 XOR C3. Each custodian generates or receives one
random component, recorded on tamper-evident forms. Each component has a
**Key Check Value (KCV)**: first 3 bytes of AES-ECB(Ci, zero block) (or the
AES-CMAC-based KCV for AES per ANSI X9.24 (gated: unconfirmed, source is paywalled or blocked)), so entry errors are caught without
revealing the component. The combined key's KCV is verified after loading.

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
def kcv(k): e = Cipher(algorithms.AES(k), modes.ECB()).encryptor(); return (e.update(bytes(16))+e.finalize())[:3].hex()
```

(ECB on one zero block for a check value is the standard KCV use; not for data.)

Prefer Shamir M-of-N for root/backup keys so one absent custodian does not
block recovery; XOR components need all N.

## Dual control in modern platforms

- **HSM quorum (M of N)**: AWS CloudHSM quorum authentication (M of N, minimum 2, for operations such as HSM user management by crypto officers; the requester may supply one of the approvals); Luna PED keys with M-of-N; nShield Operator Card Sets (k of n).
- **Cloud KMS**: no built-in two-person approval on `Decrypt`, but you can
  require it for key policy changes and deletion via change-management
  (IAM conditions + approval workflow, AWS IAM Identity Center with
  just-in-time access, GCP PAM entitlements with approvers).
- **Vault**: Control Groups (Enterprise licence required) require approvals for a path; unseal
  and root token generation use Shamir shares.

## Separation of duties in IAM

- Key administrators: can create, rotate, disable, change policy, but have no
  `kms:Decrypt`/`Encrypt` (AWS key policy separates "key administrators" from
  "key users").
- Key users: the application roles; no policy-change rights.
- Auditors: read-only on logs.
- Break-glass: a separately monitored role requiring two approvers.

## Verify

- [ ] No IAM principal holds both key admin and key use on the same key (policy scan).
- [ ] Component custodians recorded, KCVs logged, combined KCV verified.
- [ ] HSM quorum / approval workflow tested with an actual M-of-N operation.
