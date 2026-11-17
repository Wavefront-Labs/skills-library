---
id: computing-software.cryptography-implementation.key-management.destroyed-versus-destroyed-compromised-states
name: destroyed-versus-destroyed-compromised-states
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, destroyed-compromised-state, key-states, sp-800-57, key-destruction, key-lifecycle]
level: practitioner
status: docs-checked
description: "Handle SP 800-57 destroyed keys and the optional destroyed-compromised state: when compromise is learned after destruction, what metadata to keep, and old signatures."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destroyed versus destroyed-compromised states

SP 800-57 Part 1 Rev. 5 section 7 defines pre-activation, active, suspended, deactivated, compromised and
destroyed states. It notes that systems may add states, and names a "destroyed compromised" state, shown in an
example in an earlier version, as one such addition. So destroyed-compromised is an optional extra, not a
required state of the current standard.

## Meaning
- **Destroyed**: the key no longer exists. Metadata (for example state transition history, key name, type,
  cryptoperiod) may be retained for audit (section 7.6, section 8.4).
- **Destroyed compromised** (optional extra state): the key is destroyed and was known or suspected to be
  compromised, before or after destruction.
- The standard says a compromise of a destroyed key can be determined after destruction; in that case the event
  shall be recorded (logging per SP 800-152).

## Why the difference matters
- A compromised key must never apply protection. Verifying earlier signatures with the public key of a compromised
  private key is allowed only under highly controlled conditions, for example when the signed data was physically
  protected before the compromise or carries a reliable timestamp.
- Record the compromise date so relying parties can tell which signatures predate it.

## Practice
- Keep a metadata record after destruction (section 7.6, 8.4).
- Fields: state, destruction date, method/evidence, compromise date (if any), reason.
- If you add a destroyed-compromised state, never move a key from it back to plain destroyed.

## Verify
- [ ] Key inventory can record a compromise discovered after destruction, with a compromise date field.

## Checked
Date: 2026-11-01. Confirmed in NIST SP 800-57 Part 1 Rev. 5: section 7 states list and the note that a destroyed
compromised state came from an earlier version, section 7.5 (controlled-condition use with timestamp or protected
signature), section 7.6 (metadata retained, later-discovered compromise recorded). Corrected: the earlier draft said
section 7 defines destroyed compromised; it does not in Rev. 5. Removed: the KMIP state-transition claims and the
SP 800-130 source (not checked), CRL claims.
Method: documentation only; no commands were run.
