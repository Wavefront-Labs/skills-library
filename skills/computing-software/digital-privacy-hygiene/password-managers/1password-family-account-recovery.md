---
id: computing-software.digital-privacy-hygiene.password-managers.1password-family-account-recovery
name: 1password-family-account-recovery
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, 1password-account-recovery, vault-recovery, family-vault]
level: practitioner
status: draft
description: "Recover a locked-out 1Password family member: organiser starts recovery, member gets a new Secret Key, and why you need two organisers."
sources:
  - "https://support.1password.com/recovery/"
  - "https://support.1password.com/family-organizer/"
  - "https://support.1password.com/secret-key/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# 1Password family account recovery

**Goal:** a family member who forgot their account password or lost their Secret Key gets back in without losing
their data.

## Who can recover whom
- Family organisers can recover family members.
- An organiser can only be recovered by **another organiser**. Make at least two adults organisers.

## Steps
1. Organiser signs in at 1Password.com > People > select the member > **Begin Recovery**.
2. Member receives an email, opens the link on a trusted device, creates a **new account password**, and gets
   a **new Secret Key** (and a new Emergency Kit to save).
3. Organiser gets a notification and clicks **Complete Recovery** (this confirms the new key exchange).
4. Member signs in on each device again with the new password and Secret Key.

## What the organiser can and can't see
Recovery restores the member's access; it doesn't give the organiser the member's private vault contents.

## After recovery
- Print/save the new Emergency Kit; destroy the old one.
- Check that 2FA on the 1Password account (if enabled) still works or re-enroll.

## Gotchas
- If nobody else is an organiser and the sole organiser forgets everything, 1Password cannot help.
- Phishing emails imitate recovery messages: the member should go to 1Password.com directly if unsure.
