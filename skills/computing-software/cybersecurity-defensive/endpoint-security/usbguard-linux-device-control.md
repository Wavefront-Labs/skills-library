---
id: computing-software.cybersecurity-defensive.endpoint-security.usbguard-linux-device-control
name: usbguard-linux-device-control
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [device-control, usbguard, linux, usb-allowlist, badusb, rules-conf, removable-media-policy]
level: practitioner
status: docs-checked
description: "Lock down USB on Linux with USBGuard: generate an initial policy, write rules by ID, serial, hash and interface class, reject combo devices, restrict IPC access, and audit."
sources: ["https://usbguard.github.io/documentation/rule-language.html", "https://usbguard.github.io/documentation/configuration.html", "https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/protecting-systems-against-intrusive-usb-devices_security-hardening"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# USBGuard on Linux

USBGuard protects systems against intrusive USB devices using allow and block lists built on the kernel's USB
device authorization feature.

## Install and baseline
```
dnf install usbguard
usbguard generate-policy > /etc/usbguard/rules.conf   # allow policy for everything currently attached
systemctl enable --now usbguard
```
Review the generated rules before use. The upstream workflow is: generate to a file, edit, then
`sudo install -m 0600 -o root -g root rules.conf /etc/usbguard/rules.conf` and restart the service.
Generate with the devices you trust plugged in. `generate-policy` adds `via-port` to devices without a serial
(unless `-P`), `-t <target>` adds an explicit catch-all rule, `-X` omits hashes.

## Rule language
```
allow id 1d6b:0002 serial "0000:00:14.0" name "xHCI Host Controller" with-interface 09:00:00
allow with-interface equals { 08:*:* }                  # only single-interface mass storage devices
reject with-interface all-of { 08:*:* 03:00:* }         # storage + HID combo (suspicious)
reject with-interface all-of { 08:*:* 03:01:* }
```
- Rules are scanned in order; the first match decides. With no match, the implicit target applies.
- Attributes: `hash` (computed by USBGuard; the most specific way to match one device), `name`, `serial`,
  `via-port`, `with-interface` (class:subclass:protocol, `*` allowed for subclass and protocol together).
- Set operators for sets: `all-of`, `one-of`, `none-of`, `equals`, `equals-ordered`.
- Targets: `allow` authorizes, `block` deauthorizes ("do not interact with this device for now"), `reject`
  removes the device as if it did not exist.
- Upstream warns that blacklisting is the wrong approach: block by default and allow known devices.

## Daemon config (/etc/usbguard/usbguard-daemon.conf)
- `ImplicitPolicyTarget` (default `block`), `PresentDevicePolicy` (default `apply-policy`),
  `InsertedDevicePolicy` (default `apply-policy`).
- IPC access: set `IPCAccessControlFiles` (recommended), or `IPCAllowedUsers` / `IPCAllowedGroups`
  (e.g. `IPCAllowedGroups=wheel`). Do not leave the ACL unconfigured: all local users could then change
  device authorization and the policy.
- `RestoreControllerDeviceState=true` can let an attacker who shuts the daemon down revert to the permissive OS
  default; upstream flags this as a risk.
- `AuditBackend` is `FileAudit` (default) or `LinuxAudit`; `HidePII=true` hides serials and hashes from audit entries.

## Operations
```
usbguard list-devices
usbguard allow-device <id>
usbguard block-device <id>
usbguard reject-device <id>
usbguard allow-device <id> -p      # -p adds a device-specific rule to the policy
```
Permanent changes need the daemon to be able to write rules; on SELinux systems the
`usbguard_daemon_write_rules` boolean controls this (Red Hat guide).
Exception workflow: user requests, admin allows by hash for that host, change recorded.

## Gotchas
- Devices not in the baseline fall to the implicit target (block by default), so include keyboards, mice and
  internal devices in the baseline, and test a policy with console access before applying it to a remote server.

## Verify
Insert an unknown USB stick: `usbguard list-devices` shows it as `block`.

## Checked
2026-11-01. Confirmed against USBGuard Rule Language and Configuration pages and Red Hat's RHEL 9 USBGuard chapter (install, generate-policy, allow/block/reject-device, `-p`, SELinux boolean, IPC warning). Removed: apt package name, interface-class list beyond 08/03/e0/02, `usbguard watch`, docking-station and GNOME advice, `lsblk` check, auditd claims.
Method: documentation only; no commands were run.
