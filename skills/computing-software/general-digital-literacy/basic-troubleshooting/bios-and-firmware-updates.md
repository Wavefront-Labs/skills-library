---
id: computing-software.general-digital-literacy.basic-troubleshooting.bios-and-firmware-updates
name: bios-and-firmware-updates
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-updates, firmware-update, bios-update, uefi]
level: intro
status: draft
description: "Decide whether to update a PC BIOS/UEFI or device firmware, do it safely with the maker's tool on mains power, and recover if it fails; plus Macs, routers and docks."
sources:
  - https://support.microsoft.com/en-us/windows/update-drivers-manually-in-windows-ec62f46c-ff14-c91d-eead-d7126dc1f7b6
  - https://www.dell.com/support/kbdoc/en-us/000124211/dell-bios-updates
  - https://support.apple.com/en-us/102657
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# BIOS and firmware updates

## When to update
- To fix a listed problem (crashes, battery drain, sleep failures, USB-C dock issues), a **security advisory** for your model, or to support new hardware (CPU, Windows 11 TPM/Secure Boot).
- Not because a newer version exists and everything works.

## PC laptops and desktops
- Use the **maker's tool**: Dell SupportAssist / Dell Command Update, HP Support Assistant, Lenovo Vantage / System Update, ASUS MyASUS / EZ Flash, Acer support site. Many also arrive via **Windows Update › Advanced options › Optional updates › Driver updates** ("Firmware").
- Find current version: `msinfo32` › *BIOS Version/Date*.
- Rules: laptop **plugged in** with battery >50%; close apps; suspend BitLocker if the tool doesn't (Control Panel › BitLocker › Suspend protection) or you'll be asked for the recovery key; do not power off during the update (screen may go black and fans roar for minutes).
- Desktop motherboards: download the exact board/revision file; flash from the BIOS's own utility via USB.

## If it fails
- Many modern boards have **dual BIOS / BIOS recovery** (Dell: hold Ctrl+Esc at power-on; HP: Win+B; ASUS: BIOS FlashBack USB port). Otherwise it's a repair job.

## Other firmware
- **Mac**: firmware comes with macOS updates; nothing separate.
- **Routers**: admin page or app › Firmware update; enable auto-update.
- **SSDs**: Samsung Magician, Crucial Storage Executive, WD Dashboard (back up first).
- **Docks, monitors, mice**: maker apps (Dell Display Manager, Logi Options+).

## Verify
- [ ] `msinfo32` shows the new version; the original problem is gone; BitLocker resumed.
