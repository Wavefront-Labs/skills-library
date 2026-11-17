---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.reading-smart-data-and-drive-health
name: reading-smart-data-and-drive-health
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, storage-troubleshooting, smart-status, smartctl, crystaldiskinfo, get-physicaldisk, reallocated-sectors, nvme-health, percentage-used, drive-failure-prediction, comptia-a-plus]
level: practitioner
status: draft
description: "Judge whether an HDD or SSD is failing from SMART: key attributes and NVMe health fields, smartctl and PowerShell, and thresholds that justify replacement."
sources:
  - "https://www.smartmontools.org/wiki/TocDoc"
  - "https://learn.microsoft.com/en-us/powershell/module/storage/get-storagereliabilitycounter"
  - "https://nvmexpress.org/specifications/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# reading-smart-data-and-drive-health

Goal: decide "replace this drive now" from data, before it takes the user's
day with it.

## Read it
```powershell
Get-PhysicalDisk | Select FriendlyName, MediaType, HealthStatus, OperationalStatus
Get-PhysicalDisk | Get-StorageReliabilityCounter |
  Select DeviceId, Temperature, Wear, ReadErrorsUncorrected, WriteErrorsUncorrected, PowerOnHours
```
```bash
smartctl -a /dev/sda          # SATA
smartctl -a /dev/nvme0        # NVMe
smartctl -t short /dev/sda    # self-test, then -l selftest for result
```
CrystalDiskInfo (Windows GUI) summarises as Good / Caution / Bad. Vendor
tools (Samsung Magician, Dell/HP/Lenovo diagnostics) add firmware updates.

## Attributes that matter (SATA)
| ID | Attribute | Meaning |
|---|---|---|
| 5 | Reallocated_Sector_Ct | sectors remapped — any growth = media failing |
| 187 | Reported_Uncorrect | uncorrectable errors seen by host |
| 188 | Command_Timeout | can also be cable/power |
| 197 | Current_Pending_Sector | unstable sectors awaiting remap — serious |
| 198 | Offline_Uncorrectable | unreadable sectors |
| 199 | UDMA_CRC_Error_Count | cable/connector, not the drive |
| 177/231/233 | Wear levelling / life left (SSD, vendor-specific) | remaining endurance |
Raw values matter more than the normalised "VALUE/THRESH" columns; the
overall "PASSED" only trips at the vendor threshold, often too late.

## NVMe health log
`Critical Warning` (non-zero = act), `Percentage Used` (endurance consumed;
100 % = rated life reached, not instant death), `Available Spare` vs
threshold, `Media and Data Integrity Errors` (>0 = concern), `Unsafe
Shutdowns`, temperature.

## Decision rules
- Replace: pending/uncorrectable/reallocated counts rising between two
  reads, NVMe critical warning, media errors, failed self-test.
- Investigate cable/power first: CRC errors, command timeouts alone.
- Healthy SMART doesn't prove a healthy drive — ~1/3 of failures show no
  SMART warning; symptoms (freezes, Event ID 7/51/153 disk errors, 129
  storport resets) count too.

## Gotchas
- RAID controllers hide SMART; use the controller's tool (`smartctl -d
  megaraid,N`) or vendor management.
- USB enclosures often don't pass SMART through (`-d sat` sometimes works).

## Verify
Record the key raw values in the ticket; re-read after a week of use for
trend, or after replacement confirm the new drive reports zero errors.
