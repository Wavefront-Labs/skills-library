---
id: computing-software.it-support-helpdesk.desktop-support.macos-desktop-support
name: macos-desktop-support
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, macos, apple, filevault, kernel-panic, safe-mode, recovery-mode, disk-utility, apfs, smc-reset, nvram-reset, console-app, sysdiagnose, system-settings, gatekeeper, permissions, spctl, activation-lock, apple-silicon, t2-chip, time-machine, macos-unified-log]
level: practitioner
status: draft
description: "Troubleshoot macOS endpoints: boot modes, logs, disk repair, FileVault, kernel panics, permission and update failures, Apple Silicon quirks."
sources:
  - "https://support.apple.com/guide/mac-help/welcome/mac"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macos-desktop-support

Goal: diagnose and fix the macOS-side faults a Windows-trained helpdesk tech
will not have muscle memory for, without wiping a user's data.

## Boot modes (know which key, and that Apple Silicon differs from Intel)
- **Safe Mode**: Intel — hold Shift at boot. Apple Silicon — shut down, hold
  power until "Loading startup options", pick the volume, hold Shift and
  click "Continue in Safe Mode". Disables non-Apple kexts/login items and
  rebuilds the font cache; use it to isolate a third-party kernel extension
  or launch agent causing a panic.
- **Recovery Mode**: Intel — Cmd+R at boot. Apple Silicon — hold power at
  shutdown until options appear, then Options. Gives Disk Utility, Terminal,
  reinstall macOS, and (Apple Silicon only) a way to reinstall the OS even
  if the disk is unreadable.
- **1 Tap on Startup Security Utility (Apple Silicon, inside Recovery)**
  controls secure boot policy — if a user can't boot an external disk or a
  downgraded OS, check this before assuming hardware failure.
- No more NVRAM reset key combo on Apple Silicon (no T2/no PRAM in the old
  sense); on Intel, Option+Cmd+P+R still resets NVRAM for display/startup-disk
  corruption. SMC reset (Intel, no T2 chip: Shift+Ctrl+Option+power 10s) fixes
  fan/battery/sleep weirdness; machines with the T2 chip or Apple Silicon have
  no user SMC reset — power-cycle instead.

## Disk repair (APFS, not HFS+ assumptions)
- Disk Utility → First Aid repairs the APFS container and volumes; run it
  from Recovery if the boot volume itself is suspect (can't repair a mounted
  live boot volume fully).
- `diskutil verifyVolume /` / `repairVolume` from Terminal in Recovery for
  the same checks headless.
- A "container" holds multiple APFS volumes (System, Data, Preboot,
  Recovery, VM) sharing free space — low "disk space" complaints are often
  Preboot/snapshot bloat (local Time Machine snapshots), not real data;
  `tmutil listlocalsnapshots /` and `tmutil deletelocalsnapshots <date>`
  reclaims it.

## FileVault
- Check status: `fdesetup status`. If a user is locked out, the recovery key
  (personal or institutional, escrowed in Jamf/Intune/ABM if MDM-managed) is
  the only way in — there is no password reset bypass. Pull the institutional
  key from the MDM console before telling the user it's unrecoverable.
- Encryption/decryption progress: `diskutil apfs list` shows encryption
  state; initial encryption runs in the background and can look like "disk
  is slow" for hours on first enablement — expected, not a fault.

## Kernel panics
- Panic logs land in `/Library/Logs/DiagnosticReports/*.panic` and are also
  visible in **Console.app → Crash Reports**. Look at the "Kernel Extensions
  in backtrace" section first — a third-party kext (old VPN clients, antivirus,
  some printer drivers) is the usual cause, not Apple frameworks.
  Apple Silicon panics are rarer since most legacy kexts were replaced by
  system extensions; a panic there is a stronger hardware-failure signal.
- `sysdiagnose` (Shift+Ctrl+Option+Cmd+period, or `sudo sysdiagnose` in
  Terminal) captures a full diagnostic bundle for escalation to Apple/vendor
  — takes several minutes, warn the user.

## Logs and general diagnosis
- **Console.app** is the macOS Event Viewer — filter by process, and use the
  "Include Info/Debug Messages" toggle for transient issues that don't
  normally log.
- `log show --predicate '...' --last 1h` from Terminal for scripted log pulls
  (e.g. `log show --predicate 'eventMessage contains "wifi"' --last 30m`).
- Gatekeeper/notarization blocks ("app can't be opened because it is from an
  unidentified developer"): check with `spctl -a -v /Applications/App.app`;
  override per-app via System Settings → Privacy & Security → open anyway
  (post-Ventura it's no longer a simple right-click override on first run).
- Permission prompts failing silently (app can't access camera/mic/files):
  reset with `tccutil reset <Service> <bundle-id>` then relaunch — a stuck
  TCC database entry is a common "it just doesn't work" complaint with no
  error message.

## Updates and MDM-managed Macs
- Stuck Software Update: check `softwareupdate --history` and
  `/var/log/install.log`; a half-applied update after a forced restart
  usually resolves itself on next boot — don't reinstall the OS as a first
  move.
- If Jamf/Intune-managed, confirm the device isn't blocked by a deferred
  update policy before troubleshooting as if it were a local fault.

## Gotchas
- Activation Lock (Find My) survives a factory erase if removed from an
  Apple ID without first unenrolling — always deauthorize in Find My or ABM
  before wipe/reissue, or the next user is locked out at setup.
- `sudo` on a managed Mac may be disabled by MDM policy (SIP + managed login)
  — don't assume a "permission denied" is a broken account.

## Verify
- Boots to desktop, First Aid reports no errors, `fdesetup status` shows
  expected state, and the original complaint (panic, slow disk, blocked app)
  does not recur after one full reboot cycle. Note anything escalated to
  Apple hardware diagnostics (AHT: hold D at boot) as unresolved locally.
