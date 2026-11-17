---
id: computing-software.digital-privacy-hygiene.device-hardening.personal-device-hardening-checklist
name: personal-device-hardening-checklist
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, windows, macos, ios, android, bitlocker, device-encryption, recovery-key, filevault, windows-hello, microsoft-defender, gatekeeper, macos-firewall, lockdown-mode, stolen-device-protection, find-my, play-protect, screen-lock, app-permissions, standard-user, automatic-updates, router-security, wpa3, wps, router-firmware, backups, 3-2-1-backup, end-of-support, windows-10-end-of-life]
level: practitioner
status: draft
description: "Harden personal Windows, macOS, iOS and Android devices and the home router: encryption with saved recovery keys, updates, screen lock, permissions, backups, end-of-support."
sources:
  - "https://support.apple.com/guide/mac-help/protect-data-on-your-mac-with-filevault-mh11785/mac"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Personal device hardening checklist

**Goal:** a lost or stolen device reveals nothing, known exploits are patched before
they're used, and a dead disk or ransomware costs you a restore, not your data.

## 1. Every device
- **Automatic updates on** for the OS, browser and apps; restart when asked.
- **Screen lock**: laptops lock after ≤ 5 minutes idle, phones ≤ 1 minute; lock
  manually when you walk away (`Win+L`, macOS `Ctrl+Cmd+Q`).
- **Review app permissions** quarterly: camera, microphone, location, contacts,
  photos, accessibility/screen recording (the last two are high-risk on desktops).
- Remove apps and browser extensions you don't use.
- **End of support = replace or migrate.** No security patches means every new
  flaw stays open. Windows 10 support ended 14 Oct 2025; the consumer Extended
  Security Updates year ran to Oct 2026, so plan for Windows 11, Linux or new hardware.
  Phones get a fixed number of years of updates — check the maker's policy before buying.

## 2. Windows 10/11
- **Encryption**: Settings › Privacy & security › **Device encryption** (Home, on
  supported hardware) or **BitLocker** (Pro: Control Panel › BitLocker Drive
  Encryption). Confirm it shows *on*.
- **Recovery key**: if signed in with a Microsoft account it is usually saved at
  aka.ms/myrecoverykey. Check it is actually listed there and keep a second copy
  offline. Without it, a firmware update or motherboard swap can lock you out for good.
- **Windows Hello** PIN/face/fingerprint instead of a password at the lock screen.
- **Microsoft Defender** (Windows Security) on, with real-time protection and
  Tamper Protection; enable **Memory integrity** under Device security › Core isolation
  if your drivers allow it. A second antivirus is unnecessary for most people.
- **Daily work as a standard user**; keep a separate admin account for installs.

## 3. macOS
- **FileVault**: System Settings › Privacy & Security › FileVault › On. Store the
  recovery key offline or allow iCloud recovery — decide deliberately.
- **Gatekeeper**: leave "Allow applications from" at App Store & Known Developers.
  Recent macOS versions removed the Control-click bypass; a blocked app now needs
  Privacy & Security › "Open Anyway" — treat that as a deliberate decision.
- **Firewall**: System Settings › Network › Firewall › On.
- **Lockdown Mode** (Privacy & Security) is for people at risk of targeted spyware;
  it breaks some features, so most users don't need it.

## 4. iPhone / iPad
- **Passcode**: Settings › Face ID & Passcode › Change Passcode › Passcode Options ›
  6+ digits or **Custom Alphanumeric**. Four digits is too weak.
- **Stolen Device Protection** on (same menu, iOS 17.3+): requires Face ID and a delay
  for sensitive changes away from familiar places.
- **Find My** and Activation Lock on; set a **SIM PIN** (Settings › Mobile/Cellular ›
  SIM PIN).
- Keep "Erase Data after 10 failed attempts" in mind if you have a good backup.

## 5. Android
- Install monthly security updates (Settings › Security & privacy › updates; menu
  names vary by maker). Google Play system updates are separate — install those too.
- **Play Protect** on; avoid sideloading APKs.
- Encryption is on by default on modern devices (Android 10+) once a screen lock is
  set — use a PIN of 6+ digits or a password, not a pattern.
- Enable **Theft protection** / Find My Device features where offered, and a SIM PIN.

## 6. Home router
- Change the **admin password** from the default; disable remote administration.
- Update **firmware** (or enable auto-update); replace routers that no longer get it.
- Wi-Fi: **WPA3-Personal**, or WPA2/WPA3 mixed, or WPA2 with **AES (CCMP)** — never WEP
  or TKIP. Long passphrase.
- **Disable WPS**; disable UPnP unless something needs it. Put smart-home gadgets on
  a guest network.

## 7. Backups (3-2-1)
Three copies, two media, one off-site (see
`computing-software.general-digital-literacy.file-management.organising-files-and-folders`).
At least one copy must be offline or versioned so ransomware can't encrypt it.

## Gotchas
- Encryption without a saved recovery key is a time bomb.
- Updates deferred for "later" for weeks are the usual way devices get compromised.
- Uncertain: exact menu labels shift between OS versions and phone makers.

## Verify
- [ ] Disk encryption shows on for every laptop and phone; recovery keys located.
- [ ] All devices on a supported OS with auto-updates on.
- [ ] Screen locks within the timeouts above; phone PIN 6+ digits.
- [ ] Router admin password changed, firmware current, WPS off, WPA2-AES or WPA3.
- [ ] A restore from backup tested within the last six months.
