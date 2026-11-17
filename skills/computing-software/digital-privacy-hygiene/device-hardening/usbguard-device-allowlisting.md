---
id: computing-software.digital-privacy-hygiene.device-hardening.usbguard-device-allowlisting
name: usbguard-device-allowlisting
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, usbguard, linux-hardening, badusb, device-control]
level: practitioner
status: draft
description: "Use USBGuard on Linux to allow only known USB devices, generate a baseline policy safely, and approve new devices without locking yourself out."
sources:
  - "https://usbguard.github.io/"
  - "https://github.com/USBGuard/usbguard"
  - "https://wiki.archlinux.org/title/USBGuard"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# USBGuard device allowlisting

**Goal:** block rogue USB devices (BadUSB keystroke injectors, unknown drives) on a Linux laptop that might be left
unattended.

## Install and baseline
1. Plug in every device you normally use (keyboard, mouse, dock, YubiKey).
2. Generate a policy from what's attached:
   ```
   sudo usbguard generate-policy | sudo tee /etc/usbguard/rules.conf
   sudo chmod 600 /etc/usbguard/rules.conf
   ```
3. Check `/etc/usbguard/usbguard-daemon.conf`: `ImplicitPolicyTarget=block`, `PresentDevicePolicy=apply-policy`.
4. `sudo systemctl enable --now usbguard`.

## Day to day
```
usbguard list-devices
sudo usbguard allow-device <id>        # this session
sudo usbguard allow-device -p <id>     # permanent, adds a rule
sudo usbguard block-device <id>
```
Desktop applets (usbguard-notifier) show a prompt when a new device is plugged in.

## Rules
Rules match vendor/product IDs, serial, port and interface class. Tighten keyboards to the exact serial and port where
possible, and block devices that claim both storage and keyboard interfaces.

## Gotchas
- Generate the policy before enabling, or your keyboard may be blocked at the next boot. Keep an SSH session or a
  known-allowed keyboard handy.
- Docks and hubs present several devices; allow each.
- Device IDs can be spoofed; USBGuard raises the bar, it doesn't stop a determined attacker with your model numbers.
