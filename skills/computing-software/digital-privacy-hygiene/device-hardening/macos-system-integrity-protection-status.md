---
id: computing-software.digital-privacy-hygiene.device-hardening.macos-system-integrity-protection-status
name: macos-system-integrity-protection-status
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, system-integrity-protection, macos-security, startup-security-utility]
level: practitioner
status: docs-checked
description: "Know what System Integrity Protection covers on a Mac and check that Apple silicon startup security is still Full Security, treating unexpected changes as suspicious."
sources:
  - "https://support.apple.com/en-us/102149"
  - "https://support.apple.com/guide/security/system-integrity-protection-secb7ea06b49/web"
  - "https://support.apple.com/guide/mac-help/change-startup-disk-security-settings-mchl768f7291/mac"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# macOS System Integrity Protection status

**Goal:** confirm the Mac's core protections haven't been turned off (by you long ago, by a tool, or by an attacker).

## What SIP is
System Integrity Protection (SIP) restricts the root user and limits what root can do on protected parts of macOS.
Apple lists these protected locations: /System, /usr, /bin, /sbin, /var and the apps pre-installed with macOS.
Third-party apps and installers can still write to /Applications, /Library and /usr/local. Modification of the
protected parts is meant to be allowed only to processes signed by Apple with special entitlements, such as Apple
software updates and installers. SIP also helps prevent software from selecting a startup disk.

SIP is a computer-specific setting and is on by default (introduced in OS X El Capitan, 10.11). On an Intel-based Mac,
turning SIP off removes protection for all partitions on the physical storage device. On a Mac with Apple silicon it
is separate from, and additional to, hardware-based Kernel Integrity Protection.

## Check Apple silicon startup security
Startup Security Utility is in the Recovery app (Utilities menu):
1. Shut down, press and hold the power button until "Loading start-up options" appears.
2. Click Options, then Continue; select a startup disk and an administrator account and enter its password.
3. Choose Utilities > Startup Security Utility, select the system, unlock it if FileVault is on, click Security Policy.

Full Security is the default and means only the current OS, or signed OS software currently trusted by Apple, can
run. Reduced Security lets any version of signed OS software ever trusted by Apple run, and is needed before a
legacy kernel extension can be installed (with the option "Allow user management of kernel extensions from
identified developers"). Restart for a change to take effect.

## If it was lowered
1. Ask why: a legacy kernel-extension tool may have required Reduced Security. If you don't need it, set Full Security
   again using the steps above.
2. A managed Mac may have Reduced Security set on purpose to authorise remote management of kernel extensions and
   automatic software updates by a device management service.

## Suspicious signs
Reduced Security set when you never changed it, or a legacy kernel extension you don't recognise.

## Gotchas
- Some legitimate low-level tools need Reduced Security on Apple silicon; document it if so.
- Restoring a setting doesn't remove malware already installed; scan and consider a clean reinstall.

## Checked
Confirmed against the three cited Apple pages: protected and writable locations, root restriction, default-on and
Intel behaviour, Full and Reduced Security definitions, the Recovery steps and the kernel-extension options.
Removed: the csrutil, spctl and kmutil commands and their outputs, the Cmd+R recoveryOS key for Intel, and the
Gatekeeper check, because none of the cited pages state them.
Method: docs-only read of cited pages, 2026-11-08
