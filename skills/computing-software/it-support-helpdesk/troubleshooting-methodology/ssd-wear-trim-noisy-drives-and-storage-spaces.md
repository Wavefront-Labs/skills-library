---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.ssd-wear-trim-noisy-drives-and-storage-spaces
name: ssd-wear-trim-noisy-drives-and-storage-spaces
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, ssd-trim, drive-noise, windows-storage-spaces, ssd-wear, hdd-failure, storage-pools]
level: practitioner
status: draft
description: "Assess drive health beyond SMART basics: SSD wear and TRIM checks, clicking or grinding HDDs as failure signals, and Windows Storage Spaces pool health and repair."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil-behavior"
  - "https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/overview"
  - "https://learn.microsoft.com/en-us/powershell/module/storage/get-storagereliabilitycounter"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ssd-wear-trim-noisy-drives-and-storage-spaces

## SSD wear and TRIM
- TRIM lets the OS tell the SSD which blocks are free; without it write speed degrades.
  Check: `fsutil behavior query DisableDeleteNotify` (0 = TRIM enabled for NTFS/ReFS).
- Windows "Optimize Drives" (`dfrgui`) retrims SSDs weekly; it doesn't defragment them.
  `Optimize-Volume -DriveLetter C -ReTrim -Verbose` runs it manually.
- Wear: `Get-PhysicalDisk | Get-StorageReliabilityCounter | Select Wear, Temperature,
  ReadErrorsUncorrected` (Wear = percentage used, if the drive reports it); vendor
  tools (Samsung Magician, Crucial Storage Executive, Intel/Solidigm) show endurance
  and firmware updates. Plan replacement as "percentage used" approaches 100% or
  media errors appear.
- Full SSDs slow down; keep 10-20% free.
- Linux: `systemctl status fstrim.timer`; `sudo fstrim -av`.

## Noisy HDDs
| Noise | Meaning | Action |
|---|---|---|
| Regular clicking / "click of death" | Head failing to read, retrying | Stop using; image with ddrescue or send for recovery if data matters |
| Grinding / scraping | Head touching platters | Power off immediately; professional recovery only |
| Spin up, spin down repeatedly | Not enough power, or head/firmware fault | Check power/cable; then treat as failing |
| Loud whine/hum | Bearing wear | Back up and replace |
- Every power-on of a mechanically failing drive risks more damage; don't run chkdsk
  or repeated diagnostics on it.

## Storage Spaces
- Pools physical disks; virtual disks with resiliency (simple, two-way/three-way mirror,
  parity). Used on desktops/workstations and small servers.
- Health: `Get-StoragePool`, `Get-VirtualDisk | Select FriendlyName,
  OperationalStatus, HealthStatus`, `Get-PhysicalDisk | Select FriendlyName,
  HealthStatus, OperationalStatus, Usage`.
- Failed disk: add the replacement to the pool (`Add-PhysicalDisk`), retire the failed
  one (`Set-PhysicalDisk -Usage Retired`), `Repair-VirtualDisk`, watch
  `Get-StorageJob`, then `Remove-PhysicalDisk`.
- Parity spaces on desktops are slow for writes; mirror for performance.
- Storage Spaces is not a backup.

## Verify
TRIM is enabled and SSD wear is within limits; noisy drives are replaced with data
secured; Storage Spaces virtual disks report Healthy after repair jobs finish.
