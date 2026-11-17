---
id: computing-software.it-support-helpdesk.desktop-support.desktop-component-replacement
name: desktop-component-replacement
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, desktop-component-replacement, cmos-battery, wireless-card, psu-replacement, gpu-replacement, motherboard-replacement]
level: practitioner
status: draft
description: "Replace desktop PSU, GPU and motherboard, laptop wireless cards and CMOS batteries safely: compatibility checks, ESD practice, BitLocker and licensing gotchas, and testing."
sources:
  - "https://www.comptia.org/en/certifications/a/"
  - "https://www.dell.com/support/kbdoc/en-us/000130119/how-to-replace-the-cmos-battery"
  - "https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/recovery-overview"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# desktop-component-replacement

## Before opening anything
- Back up / confirm data is synced; record BitLocker recovery key; note BIOS settings.
- Check warranty: opening a device under warranty may need the vendor (or authorised
  technician status).
- ESD: wrist strap to chassis ground or touch bare metal; work on an ESD mat; unplug
  power and hold the power button to drain; remove laptop battery or disconnect internal
  battery connector first.

## Desktop PSU
- Match form factor (ATX, SFX, vendor proprietary in small-form-factor PCs), wattage
  with headroom (sum of components + 30%), connectors (24-pin, EPS 8-pin CPU, PCIe for
  GPU, SATA). Vendor OEM PCs often need a vendor part.
- Test suspected PSU with a PSU tester or swap; never open a PSU.

## GPU
- Physical fit (length, slot width), PCIe power connectors, PSU capacity, and
  case airflow. Uninstall the old driver (DDU in safe mode for vendor swaps
  between NVIDIA/AMD), install the card, then the current driver.

## Motherboard
- Same model from the vendor for OEM PCs. Expect: Windows reactivation (digital licence
  tied to the board; OEM licences may need vendor support or the Activation
  troubleshooter), **TPM change triggers BitLocker recovery** and Windows Hello/
  credential resets, Autopilot hardware hash changes (re-register the device), service
  tag must be programmed into the new board by the vendor tool.

## Laptop wireless card (M.2)
- Check the card is replaceable (many ultrabooks solder it) and BIOS whitelist
  restrictions (some vendors block non-approved cards).
- Note antenna connectors (MAIN/AUX, or 1/2), unclip carefully with a spudger, reattach
  firmly; a loose antenna gives weak signal.
- Install the vendor driver; check `netsh wlan show drivers` for supported standards.

## CMOS battery
- Symptoms: clock resets, "CMOS checksum error", BIOS settings lost, time drift causing
  Kerberos/TLS failures.
- Usually a CR2032 coin cell; some laptops use a wired cell behind the keyboard or
  battery. Replacing it resets BIOS settings: re-apply the baseline (Secure Boot, boot
  mode UEFI, TPM, admin password) or the machine may not boot or trigger BitLocker.

## After
- POST, BIOS shows the part, OS detects it, stress test (GPU/PSU), update asset record
  with new serials; dispose of old parts and batteries properly.

## Verify
Device boots with correct date and BIOS baseline, BitLocker resumed, Windows activated,
and the replaced part passes vendor diagnostics.
