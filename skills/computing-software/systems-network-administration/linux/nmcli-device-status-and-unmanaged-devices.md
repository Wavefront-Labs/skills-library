---
id: computing-software.systems-network-administration.linux.nmcli-device-status-and-unmanaged-devices
name: nmcli-device-status-and-unmanaged-devices
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, networkmanager, nmcli-device, nm-unmanaged, nmcli-general, connectivity-check, nm-logging]
level: practitioner
status: docs-checked
description: "Troubleshoot NetworkManager with nmcli device/general views: device states, unmanaged interfaces and why, connectivity checks, reapply vs reconnect, and NM debug logging."
sources:
  - https://github.com/NetworkManager/NetworkManager/blob/main/man/nmcli.xml
  - https://github.com/NetworkManager/NetworkManager/blob/main/man/NetworkManager.conf.xml
  - https://github.com/NetworkManager/NetworkManager/blob/main/man/NetworkManager.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nmcli device views and unmanaged devices

## Status
```bash
nmcli general status                 # overall state and connectivity
nmcli device status                  # DEVICE TYPE STATE CONNECTION
nmcli device show eth0               # IPs, routes, DNS, driver, MTU actually applied
nmcli -f GENERAL.STATE,GENERAL.REASON device show eth0   # why it's in that state
nmcli connection show --active
```
## "unmanaged" devices
Causes: listed in `[keyfile] unmanaged-devices=` (NetworkManager.conf / conf.d; an entry there is strictly unmanaged and cannot be overruled with `nmcli device set ... managed yes`), a `[device]` section with `managed=`, or a udev rule setting `ENV{NM_UNMANAGED}`. The `[device*]` `managed` option is documented as the better choice when an override must stay possible.
```bash
NetworkManager --print-config | grep -A3 -i unmanaged
nmcli device set eth1 managed yes    # runtime only; add --permanent to persist, or fix the source
nmcli device set eth1 managed yes --permanent
```
`--permanent-only` sets only the persistent state, and the value `reset` clears an explicit setting. Whether container or VM bridges should be managed is a site decision; unmanaged is the safe default for devices another tool owns.

## Applying changes
- `nmcli device reapply eth0` — apply edited connection settings without tearing down the link (most settings).
- `nmcli connection up ens3` — reactivates the profile (can interrupt the link).
- `nmcli device disconnect eth0` deactivates the device; the profile is blocked from autoconnecting again until reboot or until you modify or explicitly activate it.

## Connectivity check
`[connectivity]` in NetworkManager.conf: `uri` is the web page requested to check connectivity, `interval` is in seconds (default 300) and `0` disables checking.

## Debug logging
```bash
nmcli general logging level DEBUG domains ALL     # runtime
journalctl -u NetworkManager -f
nmcli general logging level INFO domains DEFAULT   # restore
```

## Verify
- [ ] `nmcli device status` shows intended managed/unmanaged state; `device show` matches the profile after reapply.

## Checked
Checked 2026-10-25 against the NetworkManager source tree on GitHub (NetworkManager/NetworkManager main, last commit 2026-10-23): nmcli `general status`, `general logging level ... domains ...`, `device show`, `device reapply`, `device set ... managed` with `--permanent`/`--permanent-only`/`reset`, `connection show --active`, `NetworkManager --print-config`, NetworkManager.conf `[keyfile] unmanaged-devices`, `[device] managed`, udev `NM_UNMANAGED`, `[connectivity] uri/interval`. Fixed: `nmcli device set managed yes` was described as runtime-only (it has `--permanent`) and `unmanaged-devices` entries cannot be overridden by it. Removed unconfirmed claims: ifupdown `managed=false` wording and netplan renderer.

Method: documentation only; no commands were run.
