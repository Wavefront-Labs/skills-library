---
id: computing-software.digital-privacy-hygiene.privacy-configuration.phone-preparation-for-a-protest
name: phone-preparation-for-a-protest
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, protest-device-prep, high-risk-privacy, biometric-lockout, lockdown-mode, disappearing-messages, location-services, device-seizure, burner-phone]
level: practitioner
status: docs-checked
description: "Prepare a phone for attending a protest: disable biometrics, strong passcode, encryption, minimal data, Signal with disappearing messages, location off, and photo safety."
sources:
  - "https://ssd.eff.org/module/attending-protest"
  - "https://www.eff.org/deeplinks/2020/06/surveillance-self-defense-attending-protests-age-covid-19"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Phone preparation for a protest

**Goal:** go to a protest with a phone that is useful for safety and communication but
reveals little if lost, seized or tracked. Source: EFF Surveillance Self-Defense, "Attending a Protest"
(last reviewed June 26, 2026). EFF says these are general suggestions, not legal advice.

## Before
- **Encryption and passcode**: iOS and most Android devices have built-in device encryption; protect it with a strong
  password (EFF suggests 8-12 random characters that are easy to remember and type). Encryption does not cover
  external SD or flash cards, and many digital cameras cannot encrypt.
- **Turn off Face/Touch ID or fingerprint unlock**: an officer could physically force you to unlock with your face or
  fingerprint, and in the US a memorised passcode generally gives a stronger legal footing than a biometric (the law
  is in flux). iPhone: Settings > Face (or Touch) ID & Passcode, turn "iPhone Unlock" off or tap Reset Face ID.
  Pixel on Android 14+: Settings > Security & Privacy > Device Unlock > Face & Fingerprint Unlock, turn "Unlock your
  phone" off; other makers differ.
- Keep software updated, use strong passwords and two-factor authentication.
- **Back up** your data; for iPhone iCloud backups EFF suggests Advanced Data Protection, for Android a "zero
  knowledge" backup service. Carry the bare minimum of data (forensic tools such as Cellebrite are more likely to
  succeed on older or unencrypted phones).
- **Signal** for communication: end-to-end encrypted chats and groups, and messages can be set to disappear after
  being read. EFF notes that using the phone to communicate can still expose its location through connectivity.
- Consider a **secondary or prepaid phone** with little personal data that still receives security updates. In the
  US federal rules do not require ID for a prepaid SIM (your state might); most countries do. Carrying it with your
  regular phone lets the two locations be correlated.
- **Lockdown Mode** (iPhone, iOS 16 and later) or **Advanced Protection** (Android): both disable 2G support, which
  can protect against some cell-site simulators (EFF has not seen concrete evidence of their use against protests).
  Lockdown Mode also requires the device be unlocked before connecting to accessories; Advanced Protection adds a
  reboot after 72 hours locked and charging-only USB when locked.

## At the protest
- **Phone settings**: powering off, or not bringing the phone, is the simplest protection. Otherwise EFF suggests
  airplane mode, Wi-Fi and Bluetooth off, and location services off (Android: Settings > Location, and check
  Google Location History is off; iPhone: Settings > Privacy & Security > Location Services, and consider turning off
  Significant Locations under System Services). Apps may still store GPS positions and send them once back online;
  only powering the phone off prevents that. Agree a meeting spot, since you cannot message or call.
- **Camera without unlocking**: Pixel, double-press the power button; iPhone, firmly press the camera icon on the lock
  screen (older models swipe up).
- **Photos of other people**: try to get consent; otherwise obscure faces, tattoos and distinctive clothing. Blocking
  out is better than blurring, which can sometimes be reversed. Signal has a built-in blur tool (use Note to Self to
  save the result); Image Scrubber is an online tool.
- **Metadata**: screenshot the photo, or send it to yourself in Signal (which strips metadata), before posting.
- **Travel**: automated licence plate readers record plates, times and places; linked transit cards and payment
  methods can reveal attendance; walking or cycling reduces both.
- **If arrested in the US**: EFF advises saying "I want my attorney and I choose to remain silent", telling police
  you do not consent to a search of your device, and notes you can refuse to give a password but may face
  consequences.

## After
- If the device is confiscated: your attorney may seek its return if it is not held as evidence. You can revoke
  access for logged-in services (for example X: Settings and privacy > Apps and devices), but EFF warns that
  revoking access or remote wiping may risk obstruction or destruction-of-evidence charges, so speak to an attorney
  first. Check account login logs.

## Verify
- [ ] Biometrics off, passcode strong, Signal ready, backup done, location and radios planned.

## Checked
Checked 2026-11-08 against the full text of both cited EFF pages. Removed claims the pages do not make: the
"unconscious or restrained" biometrics claim, writing contacts on paper, the side-button and Android power-menu
lockdown gestures, tower dumps, and the instruction to restrict Signal groups. Added EFF's actual steps, caveats
and legal notes. Menu paths are as EFF gives them and may differ by device or OS version.
Method: documentation only; no commands were run.
