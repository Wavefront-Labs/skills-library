---
id: computing-software.cryptography-implementation.key-management.retaining-keys-for-archived-data
name: retaining-keys-for-archived-data
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-destruction, archived-key-retention, key-archive, records-retention, long-term-signature-validation, legal-hold]
level: advanced
status: docs-checked
description: "Keep decryption and verification keys usable for as long as archived data must be read: archive design, retrieval tests, re-encryption and legal holds."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retaining keys for archived data

The opposite failure to leaking keys is losing the ability to read your
own archives: a key is destroyed, or rotated away, while old records still
need decrypting for an audit or lawsuit.

## Rule

Key retention = the longest retention period of any data the key protects,
plus margin. Map each key to its data's records-retention schedule.

## Archive design (SP 800-57 Part 1 section 8.3.1)

- A key archive holds keys for recovery beyond their cryptoperiod. Not all
  keys need archiving; archive keys before the cryptoperiod ends (for
  example when the key is activated).
- Deactivated keys are not used to apply protection but may still process
  protected information (decrypt, verify).
- Keep archived key information separate from operational data, with strong
  access control, and keep multiple copies in physically separate locations.
- Protect confidentiality with an archive-encryption key. If that algorithm
  gives no integrity protection, add a separate archive-integrity key;
  the two must be different keys. Authenticated encryption with one key
  also satisfies both.
- Timestamp entries when they enter the archive, and keep metadata:
  which datasets, date ranges, algorithm.
- Table 9: keep public signature-verification keys until no longer needed
  to verify data signed with the private key; do not archive private
  signature keys.

## Alternatives to keeping old keys

- **Re-encrypt (rewrap) archives** under current keys during rotation;
  with envelope encryption only the wrapped data keys need rewrapping.
- Before an algorithm is retired, migrate archives to the new algorithm so
  you do not depend on deprecated code to read them.
- SP 800-57 also allows the system to reconstruct (re-derive) a key from
  archived information instead of archiving the key.

## Legal hold

A hold suspends scheduled destruction for affected keys. Wire the hold
flag into the deletion workflow so scheduled key deletion is blocked.
When keys are no longer required, destroy them per SP 800-57 section 8.3.4.

## Test retrieval

Periodically pick old archives, restore keys from the archive path, decrypt
and verify. An untested archive key is a guess.

## Verify

- [ ] Each key's retention end date >= retention end of its data.
- [ ] A retrieval drill has passed recently.
- [ ] Deletion workflow checks legal-hold flags.

## Checked

2026-11-01. Confirmed against SP 800-57 Pt1 Rev 5: section 8.3.1 (archive
definition, archive before cryptoperiod end, separate storage and multiple
copies, archive-encryption and archive-integrity keys must differ unless
authenticated encryption, timestamping, reconstruction option, Table 9 for
signature keys), Deactivated state definition, section 8.3.4 destruction.
Removed: vendor claims about AWS/GCP rotation behaviour, Vault and KMS
rewrap operation names, CAdES/PAdES and ETSI references, revocation-data
claim, yearly test cadence.

Method: documentation only; no commands were run.
