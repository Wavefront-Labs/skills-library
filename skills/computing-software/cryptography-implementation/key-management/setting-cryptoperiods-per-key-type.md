---
id: computing-software.cryptography-implementation.key-management.setting-cryptoperiods-per-key-type
name: setting-cryptoperiods-per-key-type
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-types-and-cryptoperiods, cryptoperiod, sp-800-57, kms, key-rotation, cryptoperiod-selection, originator-usage-period]
level: practitioner
status: docs-checked
description: "Set cryptoperiods per key type from SP 800-57 Table 1: originator versus recipient usage periods, factors that shorten them, and enforcing them in KMS."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf", "https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html", "https://cloud.google.com/kms/docs/key-rotation"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Setting cryptoperiods per key type

A cryptoperiod is how long a key may be used. SP 800-57 Part 1 Rev 5
section 5.3 splits it for symmetric keys into an **originator usage period**
(OUP, applying protection: encrypt, sign, MAC) and a **recipient usage
period** (RUP, processing: decrypt, verify).

## Suggested cryptoperiods (SP 800-57 Pt1 Table 1, abridged)

| Key type | Cryptoperiod |
|---|---|
| Private signature key | 1 to 3 years |
| Public signature-verification key | several years (depends on key size) |
| Symmetric authentication key | OUP < 2 years, RUP < OUP + 3 years |
| Symmetric data-encryption key | OUP < 2 years, RUP < OUP + 3 years |
| Symmetric key-wrapping key | OUP < 2 years, RUP < OUP + 3 years |
| Symmetric master / key-derivation key | about 1 year |
| Private key-transport key | < 2 years |
| Static key-agreement keys (private and public) | 1 to 2 years |
| Ephemeral key-agreement keys | one key-agreement transaction |

The standard notes that in some email applications a private key-transport or
static key-agreement key may be needed beyond the public key's cryptoperiod, to
decrypt stored messages. Use the full table for the remaining types.

These are suggestions. Shorten them when volume is high, exposure is high (many
hosts, software storage, many people), the algorithm is nearing end of life, or
rotation is cheap and automated.

## Enforce in tooling

- AWS KMS and GCP Cloud KMS both support rotating symmetric keys on a schedule; GCP does not support automatic
  rotation of asymmetric keys. Read the vendor rotation pages for periods and limits.
- Certificates: validity is the cryptoperiod of the subject key unless you
  reuse keys on renewal; generate a new key at each renewal.
- Record `activation_date` and `deactivation_date` in key metadata and alert
  before expiry.

## Verify

- [ ] Key management policy has a cryptoperiod table per key type with rationale.
- [ ] Every key in KMS/HSM has a rotation schedule or documented exception.
- [ ] Decrypt-only (RUP) state is used after OUP ends instead of deleting keys.

## Checked

Date: 2026-11-01. Confirmed in NIST SP 800-57 Part 1 Rev. 5: Table 1 values and its footnotes. Confirmed in the AWS
KMS rotation page (automatic rotation, rotated key decrypts with the material that encrypted) and GCP key-rotation page
(regular schedule, no automatic rotation of asymmetric keys). Removed: root CA row, the AWS 90-2560 day range and
default, GCP flag names, the Vault entry (not confirmed in the cited pages).
Method: documentation only; no commands were run.
