---
id: computing-software.cybersecurity-defensive.system-hardening.firmware-update-management
name: firmware-update-management
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [firmware-security, firmware-update-management, bios-updates, bmc-firmware, fwupd, lvfs, oem-update-tools]
level: practitioner
status: draft
description: "Manage firmware updates for servers, laptops, BMCs and peripherals: inventory versions, track vendor advisories, stage via fwupd and OEM tools, and verify after rollout."
sources: ["NIST SP 800-193 Platform Firmware Resiliency Guidelines", "Linux Vendor Firmware Service and fwupd documentation", "CISA - Hardware and firmware security guidance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Firmware update management

**Goal:** firmware (BIOS/UEFI, BMC, NIC, storage controllers, SSDs, docks, TPM) is inventoried and patched on a cadence like software.

## Inventory
- Windows: `Get-CimInstance Win32_BIOS | Select SMBIOSBIOSVersion,ReleaseDate`; Intune/ConfigMgr hardware inventory; OEM tools (Dell Command | Monitor, HP Image Assistant, Lenovo Commercial Vantage).
- Linux: `dmidecode -t bios`, `fwupdmgr get-devices`.
- Servers: Redfish API from BMCs `GET /redfish/v1/UpdateService/FirmwareInventory`; vendor consoles (Dell OpenManage, HPE OneView/iLO Amplifier, Lenovo XClarity).
- Record in CMDB per asset: model, firmware component, version, date.

## Advisories
Subscribe to OEM security bulletins (Dell DSA, HP HPSBHF, Lenovo LEN-), Intel/AMD PSIRT, BMC vendors; map CVEs to models in inventory. Vulnerability scanners detect some BMC/BIOS versions.

## Deploy
- Laptops/desktops: Windows Update for Business driver/firmware (OEM-published capsules), Intune driver updates policies, Dell Command | Update / HP / Lenovo update tools via packaging.
- Linux: `fwupdmgr refresh && fwupdmgr get-updates && fwupdmgr update` (LVFS-supported devices); automate with `fwupd-refresh.timer`.
- Servers: vendor update bundles via BMC/Redfish during maintenance windows; cluster-aware (drain node, update, validate, return).
- BitLocker: suspend for one reboot before BIOS updates (`Suspend-BitLocker -MountPoint C: -RebootCount 1`), or users hit recovery.
- Ring deployment: lab -> pilot (5%) -> broad; firmware failures can brick devices.

## Harden the update path
- Enable BIOS update signature verification and anti-rollback where offered; firmware admin password set.
- BMCs on isolated management network; change default credentials; disable IPMI-over-LAN if Redfish/HTTPS is available.

## Verify
- [ ] Compliance report: % assets on vendor-current or approved firmware per model.
- [ ] No assets running firmware with known exploited vulnerabilities beyond SLA.
