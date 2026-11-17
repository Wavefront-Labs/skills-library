---
id: computing-software.cybersecurity-defensive.network-defence.bluetooth-security
name: bluetooth-security
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [bluetooth-security, ble, bluetooth-pairing, nist-sp-800-121, device-control, wireless-security, mdm-bluetooth-policy]
level: practitioner
status: draft
description: "Manage Bluetooth risk on endpoints: pairing modes, LE Secure Connections, discoverability, MDM/GPO restrictions, allowed services, patching BLE stack flaws and detection limits."
sources: ["https://csrc.nist.gov/pubs/sp/800/121/r2/upd1/final", "https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-bluetooth", "https://support.apple.com/guide/deployment/bluetooth-payload-settings-dep7f0d7e4e9/web"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bluetooth security

## Threats
Unauthenticated pairing (Just Works) allowing MITM, stack vulnerabilities (BlueBorne, BLUFFS, BrakTooth,
KNOB key-length downgrade), data exfiltration to paired phones, keystroke injection via spoofed HID
devices, tracking via static addresses.

## Controls
| Control | How |
|---|---|
| Pairing security | Prefer LE Secure Connections / Secure Simple Pairing with numeric comparison or passkey; avoid Just Works for keyboards and sensitive devices |
| Discoverability | Non-discoverable by default; discoverable only during pairing |
| Restrict services | Windows Policy CSP `Bluetooth/ServicesAllowedList` (allow HID, audio; block OBEX file transfer UUIDs); `AllowPrepairing`, `AllowAdvertising` |
| Disable where not needed | Servers, kiosks, secure areas: disable radio via MDM/BIOS; macOS configuration profile can disable Bluetooth sharing |
| File transfer | Block Bluetooth file transfer via device control (Defender device control can block Bluetooth file transfer, or block via service UUID allow-list) |
| Patching | OS and Bluetooth firmware/driver updates; vendor bulletins |
| Mobile | MDM restrictions on Bluetooth sharing/AirDrop for managed devices |

## Detection limits
EDR sees paired device events (Windows event `Microsoft-Windows-Bluetooth-BthLEPrepairing`, Defender
`DeviceEvents` for Bluetooth policy) but not RF-level attacks; RF monitoring needs dedicated sensors.

## Gotchas
- Blocking OBEX does not stop exfil via a paired phone's tethering/network; combine with network controls.
- Restrictive allow-lists break headsets that use extra profiles; pilot.

## Verify
- [ ] Policy applied: file transfer over Bluetooth blocked on a test device.
- [ ] Bluetooth disabled on servers and in-scope kiosks.
