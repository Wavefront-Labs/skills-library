---
id: computing-software.cybersecurity-defensive.security-operations.exfiltration-hunting
name: exfiltration-hunting
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [threat-hunting, exfiltration-hunting, data-staging, rclone, cloud-storage-exfil, bytes-out-anomaly, t1567, t1048, archive-creation]
level: advanced
status: docs-checked
description: "Hunt data exfiltration using ATT&CK: staging and archiving, rclone and cloud-storage uploads, chunked transfers, unencrypted alternative protocols and DNS tunnelling."
sources: ["https://attack.mitre.org/tactics/TA0010/", "https://attack.mitre.org/techniques/T1074/", "https://attack.mitre.org/techniques/T1560/", "https://attack.mitre.org/techniques/T1567/002/", "https://attack.mitre.org/techniques/T1048/003/", "https://attack.mitre.org/techniques/T1071/004/", "https://attack.mitre.org/techniques/T1030/", "https://attack.mitre.org/software/S1040/", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exfiltration hunting

Data theft usually follows an arc that ATT&CK splits across tactics: collect, stage (T1074),
archive (T1560), then exfiltrate (TA0010). Each step leaves traces; hunt backwards from any
intrusion, since exfiltration can precede the visible impact.

## Staging and compression
- **Data Staged (T1074):** adversaries stage collected data in a central location or directory
  before exfiltration, in separate files or combined into one, to minimise connections to their
  C2 server; interactive command shells and common `cmd` or `bash` functionality copy data into
  the staging location. In cloud environments data can be staged on an instance or VM.
- **Archive Collected Data (T1560):** data is compressed and/or encrypted before exfiltration, by a
  utility (T1560.001), a library (T1560.002) or a custom method (T1560.003). Look for archiving
  utilities run by unusual accounts or on servers that never archive, creating large or
  password-protected files shortly before network egress.
```kql
DeviceProcessEvents
| where FileName in~ ("7z.exe","7za.exe","rar.exe","winrar.exe","makecab.exe","tar.exe")
| project Timestamp, DeviceName, AccountName, FileName, ProcessCommandLine
```
`DeviceName`, `AccountName`, `FileName` and `ProcessCommandLine` are `DeviceProcessEvents`
columns; add your own allowlist of backup and packaging jobs.

## Cloud storage and tools
- **Exfiltration to Cloud Storage (T1567.002):** exfiltration to a cloud storage service rather than
  the primary C2 channel; ATT&CK's examples are Dropbox and Google Docs, and it notes this gives
  cover when hosts already talk to the service.
- **Rclone (S1040):** a command-line program for syncing files with cloud storage such as
  Dropbox, Google Drive, Amazon S3 and MEGA, used in ransomware campaigns including those tied to
  Conti and DarkSide. Hunt by behaviour (a process making long, large uploads to storage
  services from hosts that never use them), not by name; renamed copies are common.

## Network
- **Data Transfer Size Limits (T1030):** data sent in fixed-size chunks or with packet sizes held below
  thresholds to avoid transfer-size alerts. Therefore compare per-host egress against its own
  baseline over time and look for many similar-sized transfers to one destination, not only one
  large upload.
- **Unencrypted non-C2 protocols (T1048.003):** data sent over natively unencrypted protocols
  (HTTP, FTP, DNS) to a location other than the C2 server, possibly encoded or compressed
  (for example base64) or embedded in protocol headers and fields.
- **DNS (T1071.004):** DNS tunnelling embeds commands and results in DNS traffic; commands can
  ride in record types such as TXT or A. DNS beacons communicate infrequently, which hides them
  in normal DNS traffic. Hunt for unusual query volume per host, many unique subdomains of one
  parent domain and rare record types.

## Gotchas
- Backup software and sync clients look like exfiltration; baseline them per host.
- TLS hides content; volume, destination, timing and the initiating process are your signals.

## Verify
Simulate with rclone uploading a test file to an approved test bucket from a lab host; confirm
process, network and proxy detections all see it.

## Checked
2026-11-08. Confirmed against ATT&CK TA0010 and the T1074, T1560, T1567.002, T1048.003,
T1071.004, T1030 and Rclone (S1040) pages, and the Defender `DeviceProcessEvents` column list.
Removed: the CISA advisory and DFIR Report sources (CISA blocked automated fetches; the DFIR
Report URL is a site front page), archive switches (`-p`, `-hp`, `-v500m`), the `PerfLogs` and
`ProgramData` staging folders, rclone flags and user-agent string, specific domains and bucket
providers, the Splunk statistical query, SharePoint/OneDrive, S3 and Exchange export operation
names, and the USN journal claim.
Method: documentation only; no commands were run.
