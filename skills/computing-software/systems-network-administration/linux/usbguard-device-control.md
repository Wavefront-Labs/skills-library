---
id: computing-software.systems-network-administration.linux.usbguard-device-control
name: usbguard-device-control
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, usbguard, usb-device-control, usb-allowlist, badusb, rules-conf, implicit-policy, stig, hardening, security, sysadmin]
level: practitioner
status: docs-checked
description: "Allowlist USB devices with USBGuard: generating a baseline policy from attached devices, rule syntax by hash/id/interface, allowing devices at runtime, and avoiding lockout of keyboards."
sources:
  - https://github.com/USBGuard/usbguard/blob/main/doc/man/usbguard-rules.conf.5.adoc
  - https://github.com/USBGuard/usbguard/blob/main/doc/man/usbguard-daemon.conf.5.adoc
  - https://github.com/USBGuard/usbguard/blob/main/doc/man/usbguard.1.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# USBGuard device control

**Goal:** only known USB devices work; a rogue stick or "keyboard" (BadUSB) plugged into
a server or kiosk is blocked, and you don't lock yourself out doing it.

## 1. Baseline from what's attached now
```bash
dnf install usbguard        # apt install usbguard
usbguard generate-policy > /etc/usbguard/rules.conf     # allow every currently connected device (via-port added only for devices without a serial; -p adds ports for all)
systemctl enable --now usbguard
usbguard list-devices                                   # each with allow/block and its rule
```
Do this with the keyboard/mouse/YubiKey you need already plugged in — anything absent is blocked once the daemon starts.

## 2. Rules
```
allow id 046d:c52b serial "" name "USB Receiver" hash "Hn3..." with-interface { 03:01:01 03:01:02 } via-port "1-2"
allow with-interface equals { 08:*:* }                              # any mass storage (example, usually too broad)
allow id 1234:5678 with-interface one-of { 03:*:* 0b:*:* }          # placeholder ID: security token with HID + smart card interfaces
block with-interface all-of { 08:*:* 03:00:* }                      # storage+keyboard combo devices = BadUSB pattern
reject with-interface one-of { 0e:*:* }                             # reject = logically remove the device
```
Interface classes are USB class codes: `03` HID, `08` mass storage, `09` hub, `0b` smart card, `0e` video, `e0` wireless. The daemon scans the rules sequentially and applies the target of the matching rule;
`ImplicitPolicyTarget` (in `usbguard-daemon.conf`, default `block`) handles devices matching no rule.
Operators for set attributes are `all-of`, `one-of`, `none-of`, `equals` (the default), `equals-ordered` and `match-all`; `*` wildcards work in IDs and interface subclass/protocol (not a specific subclass with a wildcard protocol).
Prefer matching `hash` (computed from the device attributes and descriptor data) + `id` + `with-interface`; `via-port` pins to a port, `parent-hash` to a parent device.

## 3. Runtime operations
```bash
usbguard list-devices --blocked
usbguard allow-device 7            # this time only
usbguard allow-device -p 7         # and append a permanent rule
usbguard block-device 7
usbguard watch                     # live events while plugging
```
Let a non-root admin group use the IPC: `IPCAllowedGroups=wheel` in `/etc/usbguard/usbguard-daemon.conf` (the man page lists it as the legacy form; `IPCAccessControlFiles` is the finer-grained one). The device number in `allow-device 7` is the rule ID shown first in `list-devices`, not the USB ID.

## 4. Settings worth checking
- `PresentDevicePolicy` (default `apply-policy`: evaluate devices present at daemon start; also `allow`, `block`, `reject`, `keep`).
- `PresentControllerPolicy` (default `keep`, leaves USB controllers as they are).
- `InsertedDevicePolicy` (default `apply-policy`; also `block`, `reject`).
- `AuthorizedDefault` (default `none`) sets the authorization state new devices start with on controllers.

## Gotchas
- Laptop docks/KVMs present new hubs and devices with different hashes — plug them in during baseline or write `id`-based rules.
- Remote-only servers: if the policy blocks the keyboard, the console is useless during an outage; keep a known keyboard allowed by `id`.

## Verify
- [ ] `usbguard list-devices` shows all needed devices `allow`; an unknown USB stick appears as `block` and doesn't mount.
- [ ] After reboot, keyboard and authenticators still work at the console.

## Checked

Checked 2026-10-26 against the USBGuard/USBGuard repository (last commit 2026-09-07), doc/man usbguard-rules.conf.5, usbguard-daemon.conf.5 and usbguard.1. Confirmed: rule targets and operators, sequential rule scan, wildcard rules, daemon option names and defaults (ImplicitPolicyTarget block, PresentDevicePolicy apply-policy, PresentControllerPolicy keep, InsertedDevicePolicy apply-policy, AuthorizedDefault none), generate-policy port behaviour, allow-device -p and rule-ID semantics, IPCAllowedGroups being the legacy form. Removed: the YubiKey vendor ID example (replaced by a placeholder), chmod 600 advice and the kernel authorized_default comparison.

Method: documentation only; no commands were run.
