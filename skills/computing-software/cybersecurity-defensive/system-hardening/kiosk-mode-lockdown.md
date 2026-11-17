---
id: computing-software.cybersecurity-defensive.system-hardening.kiosk-mode-lockdown
name: kiosk-mode-lockdown
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [kiosk-mode, assigned-access, single-purpose-device, shell-launcher, chrome-kiosk, lockdown]
level: practitioner
status: docs-checked
description: "Lock down kiosks and single-purpose devices: Windows Assigned Access and Shell Launcher, Linux and ChromeOS kiosk modes, escape paths to close, and physical controls."
sources: ["https://learn.microsoft.com/en-us/windows/configuration/assigned-access/", "https://learn.microsoft.com/en-us/windows/configuration/shell-launcher/", "https://support.google.com/chrome/a/answer/3273084", "https://ubuntu.com/tutorials/secure-ubuntu-kiosk"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kiosk and single-purpose lockdown

Public kiosks, digital signage, check-in terminals and shop-floor stations run one application for anonymous
or shared users. Anyone at the screen is an untrusted user; the goal is that they cannot reach anything but
that app.

## Windows
- **Assigned Access**: restricts a Windows account to the apps you allow (see the Assigned Access overview for single-app and multi-app kiosks and how to configure them).
- **Shell Launcher**: controls which application a user gets as the shell after sign-in. It does not support a custom shell whose application launches a different process and exits.
- Add an application allowlist, disable USB storage, and use auto logon only for the restricted kiosk account.

## Browser kiosks
- Browser kiosks: use the browser's managed kiosk mode (Edge via Assigned Access; ChromeOS managed kiosk apps via Google Admin, see the Chrome Enterprise help page) and block everything not needed by policy: URL allowlist, dev tools, downloads, printing, local file access, inactivity reset.

## Linux
Run only the app in a minimal Wayland kiosk shell such as Ubuntu Frame (see Canonical's secure Ubuntu kiosk tutorial); no desktop environment, TTY switching disabled, read-only root filesystem or overlay, automatic restart on crash.

## Escape paths to test
Print dialogs and "Save as" (file browsers), help links opening browsers, on-screen keyboards with settings
buttons, right-click/long-press menus, accessibility shortcuts such as Sticky Keys, error
dialogs, app crash revealing desktop, USB keyboards plugged into exposed ports, network boot, BIOS access.

## Physical and network
Enclosure covering ports and power button, BIOS/UEFI password and boot order lock, disk encryption, kiosk on an
isolated network segment with egress allowlist to the app backend only, remote management and monitoring for
tampering.

## Verify
Run an escape test checklist on the deployed build (keyboard shortcuts, dialogs, crash, USB, reboot) with none
reaching a shell, file system or other app; reboot returns to a clean state.

## Checked

2026-10-28. Confirmed against: Microsoft Learn Assigned Access overview and Shell Launcher (what each does, Shell Launcher limitation); Canonical Ubuntu Frame kiosk tutorial; Chrome Enterprise kiosk help page (existence and scope).

Removed as unconfirmed: msedge command line and edge-kiosk-type, URLAllowlist names, keyboard filter/UWF editions, Linux logind keys, cage, Sticky Keys keystroke detail.

Method: documentation only; no commands were run.
