---
id: computing-software.cryptography-implementation.key-management.key-state-model-and-transitions
name: key-state-model-and-transitions
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-types-and-cryptoperiods, key-states, sp-800-57, key-lifecycle, deactivated-key, compromised-key, kms]
level: practitioner
status: docs-checked
description: "Apply the SP 800-57 key state model: pre-activation to destroyed, allowed operations per state, and mapping states to AWS KMS and GCP Cloud KMS key states."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf", "https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html", "https://cloud.google.com/kms/docs/key-states"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key state model and transitions

SP 800-57 Part 1 Rev. 5 section 7 defines the states a key passes through. Making
them explicit is what stops "old" keys from being used to encrypt new data
and stops deletion of keys still needed to decrypt. The states are an example
model: a system may add states or leave one out (for example, not use suspended).

## States and allowed operations

| State | Protect (encrypt/sign) | Process (decrypt/verify) |
|---|---|---|
| Pre-activation | no | no (only proof of possession or key confirmation) |
| Active | yes (may be designated protect only, process only, or both) | per designation |
| Suspended | no | yes (process only) |
| Deactivated | no | in some cases, for data protected earlier |
| Compromised | no | in some cases, only under highly controlled conditions |
| Destroyed | no | no; metadata (history, name, type, cryptoperiod) may be retained for audit |

Transitions: a key enters pre-activation on generation; pre-activation ->
active when the key becomes available for use (activation date or external
event); active -> deactivated at the end of its cryptoperiod; keys can move to
compromised when integrity or confidentiality becomes suspect; deactivated or
compromised keys move to destroyed when no longer needed. A pre-activation key
that will never be needed may go straight to destroyed. Record each transition
(the standard points to SP 800-152 for logging).

## Mapping to cloud KMS states

| Platform | States |
|---|---|
| AWS KMS | Enabled, Disabled, PendingDeletion, PendingImport, Unavailable (custom key store only). After rotation, decrypt uses the key material version that encrypted the data |
| GCP Cloud KMS (versions) | ENABLED, DISABLED, DESTROY_SCHEDULED, DESTROYED; only the primary version of a symmetric key encrypts, and any enabled version decrypts |

Check the vendor page for the full state list; these are not one-to-one with the
SP 800-57 states.

## Implement in your own key store

- Store `state`, `activation_date`, `deactivation_date`, `compromise_date`
  per key; check state on every operation, not just at load.
- Encrypt only with the single Active key for a purpose; decrypt with any
  key in Active or Deactivated state.
- Transition to Compromised triggers the compromise response plan.

## Verify

- [ ] Encrypt with a deactivated key fails; decrypt succeeds.
- [ ] State changes are logged with actor and reason.

## Checked

Date: 2026-11-01. Confirmed in NIST SP 800-57 Part 1 Rev. 5 (sections 7.1 to 7.6, phases in section 8, Figure 3): the
states, protect/process rules per state, example-model wording, transitions, metadata retention. Confirmed in the AWS KMS
key-state page (Enabled, Disabled, PendingDeletion, PendingImport, Unavailable) and the GCP key-states page (ENABLED,
DISABLED, DESTROY_SCHEDULED, primary version encrypts, enabled versions decrypt). Removed: the Vault transit and X.509
rows, and the claim that suspended keys decrypt "per policy" (the standard says process only).
Method: documentation only; no commands were run.
