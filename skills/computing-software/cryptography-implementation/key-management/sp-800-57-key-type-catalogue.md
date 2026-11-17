---
id: computing-software.cryptography-implementation.key-management.sp-800-57-key-type-catalogue
name: sp-800-57-key-type-catalogue
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, sp-800-57-key-types, key-types, sp-800-57, key-inventory, key-usage]
level: practitioner
status: docs-checked
description: "Classify every key by SP 800-57 Part 1 key types (section 5.1.1): signing, authentication, encryption, wrapping, RBG, master and agreement keys, with protection needs."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SP 800-57 key type catalogue

SP 800-57 Part 1 Rev. 5 section 5.1.1 lists 19 key types. Tagging each key in your inventory with one makes
cryptoperiods, protection and destruction rules mechanical.

## The list
1. Private signature key
2. Public signature-verification key
3. Symmetric authentication key
4. Private authentication key
5. Public authentication key
6. Symmetric data-encryption key
7. Symmetric key-wrapping key
8. Symmetric random number generation key
9. Symmetric master key (derives other keys)
10. Private key-transport key
11. Public key-transport key
12. Symmetric key-agreement key
13. Private static key-agreement key
14. Public static key-agreement key
15. Private ephemeral key-agreement key
16. Public ephemeral key-agreement key
17. Symmetric authorization key
18. Private authorization key
19. Public authorization key

## Using it
- Inventory columns: key type, algorithm, size, owner, location, cryptoperiod (from Table 1), status.
- One key, one type: a key used for both signing and key transport violates 5.2 and must be split.
- Protection (section 6.1, Table 5): lists, per key type, the security service, required protection
  (confidentiality, integrity, availability), associations to protect, assurances and period of protection.
- Backup differs by type (Table 7): private signature keys are generally not backed up (a CA signing key may be
  an exception), private ephemeral key-agreement keys are not backed up, and most other types may be.

## Verify
- [ ] Every row in the key inventory has a key type from this list and a matching cryptoperiod.

## Checked
Date: 2026-11-01. Confirmed in NIST SP 800-57 Part 1 Rev. 5: the 19 key types and their names (section 5.1.1), Table 1
cryptoperiods, section 5.2 (one key, one purpose; transport plus signature example), Table 5 columns, Table 7 backup rules.
Removed: the claim that decryption keys may need archiving and the confidentiality/integrity summary of Table 5, replaced
by what the tables state.
Method: documentation only; no commands were run.
