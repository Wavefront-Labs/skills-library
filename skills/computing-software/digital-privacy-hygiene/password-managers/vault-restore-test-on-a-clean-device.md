---
id: computing-software.digital-privacy-hygiene.password-managers.vault-restore-test-on-a-clean-device
name: vault-restore-test-on-a-clean-device
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, vault-restore-test, vault-recovery, disaster-recovery, emergency-kit, encrypted-export, lockout-drill]
level: practitioner
status: draft
description: "Run an annual lockout drill: from a clean device with only your memory and the emergency kit, regain vault access and restore from backup."
sources:
  - "https://bitwarden.com/help/encrypted-export/"
  - "https://support.1password.com/emergency-kit/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vault restore test

**Goal:** prove that your recovery plan works under the realistic disaster: house fire
or theft takes all your devices at once.

## Scenario rules
You have: a borrowed/clean computer (or a fresh browser profile + new VM), your memory,
and whatever you stored **off-site** (emergency kit, recovery codes, backup key, offline
backup). You do **not** have your phone.

## Drill steps
1. **Log in to the vault account** on the clean device.
   - Needs: master password (memory), 1Password Secret Key (emergency kit), 2FA.
   - If your only 2FA is the phone authenticator, you fail here: fix by adding a
     security key kept off-site or by keeping the vault 2FA recovery code with the kit.
2. **Open your email** (password from the vault, 2FA from ...?). Note every dependency
   on the phone.
3. **Restore from backup**: import last encrypted export (Bitwarden password-protected
   JSON) into a fresh test account or KeePassXC; or open the offline `.kdbx` copy.
   Check item count and that a few TOTP codes match.
4. **Time it**: under an hour is good; note blockers.

## Record and fix
Write a one-page "if all devices are gone" card listing the order of operations
(vault -> email -> phone carrier -> bank) and what each step needs. Store it with
the emergency kit.

## Gotchas
- Don't log out of your real devices during the drill; use a separate profile/VM.
- Clean up: delete the test account or wipe the VM and any downloaded export.

## Verify
- [ ] Drill completed without the phone, within one hour.
- [ ] Every blocker found has a fix recorded and implemented.
