---
id: computing-software.digital-privacy-hygiene.device-hardening.android-verified-boot-and-bootloader-state
name: android-verified-boot-and-bootloader-state
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, verified-boot, android, bootloader, avb, oem-unlocking, used-phone]
level: practitioner
status: draft
description: "Check that an Android phone boots with verified boot intact (green/yellow, bootloader locked), spot unlocked or tampered used phones, and keep OEM unlocking off."
sources:
  - "https://source.android.com/docs/security/features/verifiedboot"
  - "https://source.android.com/docs/security/features/verifiedboot/boot-flow"
  - "https://grapheneos.org/faq"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Android verified boot and bootloader state

**Goal:** the OS that boots is the one the vendor (or your chosen OS) signed, so persistent malware cannot
hide below Android.

## Boot states (Android Verified Boot)
| State | Meaning | What you see |
|---|---|---|
| Green | Locked bootloader, vendor keys | Nothing |
| Yellow | Locked, user-installed key (e.g. GrapheneOS) | Notice with key fingerprint |
| Orange | **Bootloader unlocked**, integrity not enforced | "The bootloader is unlocked and software integrity cannot be guaranteed" |
| Red | Verification failed | Device refuses to boot or warns of corruption |

## Check
```bash
adb shell getprop ro.boot.verifiedbootstate   # green / yellow / orange
adb shell getprop ro.boot.flash.locked        # 1 = locked
fastboot getvar unlocked                      # from bootloader mode
```
Without a computer: watch the boot screen for the orange warning.

## Keep it locked
- Developer options > **OEM unlocking** should be off on a daily phone; turning it on is the first step for an
  attacker with physical access (unlocking still wipes data, which protects existing data but allows a
  backdoored OS to be flashed before handing it back).
- If you unlocked to root or try ROMs, relock with the vendor or supported-OS image when done.

## Buying used
- Orange warning or OEM unlocking already on: assume tampering; factory-flash official images and relock, or reject.
- Also confirm the IMEI is not blacklisted and Factory Reset Protection is cleared (seller removed their account).

## Gotchas
- Rooted phones fail Play Integrity: banking and payment apps stop working.
- Locking the bootloader with a modified OS bricks many devices; follow the OS's instructions exactly.

## Verify
- [ ] Verified boot state green (or yellow with a fingerprint you checked); OEM unlocking off.
