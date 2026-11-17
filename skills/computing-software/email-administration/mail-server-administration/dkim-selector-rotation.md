---
id: computing-software.email-administration.mail-server-administration.dkim-selector-rotation
name: dkim-selector-rotation
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dkim-selector-rotation, dkim-rotation, selector-rotation, dkim-key-rollover]
level: advanced
status: docs-checked
description: "Rotate DKIM keys: add a new selector, switch signing, keep the old key for in-flight mail, then remove it."
sources:
  - https://www.rfc-editor.org/rfc/rfc6376
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dkim selector rotation

**Goal:** rotate without failing mail in transit.
## Steps
1. Generate a new key pair under a new selector (for example `mail2027`) and publish its TXT record at `mail2027._domainkey.<domain>`.
2. Once the record is published, start signing with the new private key and selector straight away; the RFC advises that signing commence with the new key immediately when rotating.
3. Keep the old public key published for a reasonable validation interval before removing it, because verifiers may defer validation, perhaps until the message is read by the final recipient. The RFC does not give a number of days; choose one that covers your longest retry and delivery delays.
4. Do not sign with a key whose selector is expected to be revoked or removed before verifiers can validate the signature.
5. The rotation schedule is your policy; the RFC says all selectors are equal and the choice is a matter of administrative convenience.
## Failure modes
- Removing the old key too soon breaks verification of delayed messages.
- Signing with a selector that has no published key cannot be verified.
## Verify
- New messages show the new `s=` tag in the DKIM-Signature header and verify at a receiving system.

## Checked

2026-11-09. Confirmed on RFC 6376 section 5.2 (informative operations advice on rotating to a new key pair and retaining the old public key for a reasonable validation interval, deferred validation by verifiers, all selectors equal). Removed: KeyTable/SigningTable (OpenDKIM specifics), the "at least a few days" figure, the M3AAWG attribution (that source is not cited), the explicit dkim=fail result wording, and the boilerplate Postfix/Dovecot notes.

Method: documentation only; no commands were run.
