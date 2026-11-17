---
id: computing-software.digital-privacy-hygiene.device-hardening.before-first-unlock-and-phone-encryption-states
name: before-first-unlock-and-phone-encryption-states
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, before-first-unlock, after-first-unlock, mobile-encryption, ios, android, data-protection, lockdown]
level: practitioner
status: draft
description: "Understand Before-First-Unlock vs After-First-Unlock encryption on iPhone and Android, and power a phone off before situations where it may be seized."
sources:
  - "https://support.apple.com/guide/security/welcome/web"
  - "https://source.android.com/docs/security/features/encryption/file-based"
  - "https://ssd.eff.org/module/attending-protest"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Before-first-unlock and phone encryption states

**Goal:** know when a phone's data is genuinely locked, and put it in that state on purpose.

## The two states
- **Before First Unlock (BFU):** after a power-on or reboot, before the passcode is entered. The keys
  protecting most user data are not in memory; the Secure Enclave/Titan chip will only release them after the
  passcode. Forensic extraction is very limited.
- **After First Unlock (AFU):** once unlocked one time since boot, many keys stay available even while the
  screen is locked so background apps work. Commercial extraction tools are far more successful here.

| | iPhone | Android (file-based encryption) |
|---|---|---|
| BFU-protected | Data Protection "Complete Until First User Authentication" and "Complete" classes | Credential Encrypted (CE) storage |
| Available at boot | Minimal (alarms, some system data) | Device Encrypted (DE) storage for Direct Boot apps |

## Practice
- Power the phone **off** (not just lock it) before border crossings, protests, police interactions, or
  leaving it in a hotel.
- Quick biometric disable: iPhone, hold side + volume button until the power slider appears, then cancel;
  passcode now required. Android: power menu > **Lockdown** (enable in Settings > Display/Lock screen if missing).
  These help, but the phone is still AFU; only a reboot returns it to BFU.
- Use a strong passcode: BFU protection is only as strong as the passcode's resistance to hardware-throttled
  guessing.
- Combine with inactivity auto-reboot so a seized phone falls back to BFU on its own.

## Gotchas
- Biometrics cannot unlock a BFU phone; you may be compelled to give a fingerprint in some jurisdictions but
  BFU forces a passcode.
- Cloud backups (iCloud without Advanced Data Protection, Google backup) are outside this model entirely.

## Verify
- [ ] After a restart, iPhone shows "passcode required after restart" / Android shows "PIN required after restart".
- [ ] You know the shutdown gesture for your phone without looking.
