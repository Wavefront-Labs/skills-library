---
id: computing-software.digital-forensics-incident-response.incident-response-process.scoping-ransomware-encryption-and-exfiltration
name: scoping-ransomware-encryption-and-exfiltration
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [encryption-scoping, ransomware, data-exfiltration, double-extortion, scoping, dfir]
level: advanced
status: draft
description: "Scope a ransomware incident before restoring: which systems are encrypted, how far encryption spread, and what data was exfiltrated for double extortion."
sources: ["https://www.cisa.gov/stopransomware/ransomware-guide", "https://attack.mitre.org/techniques/T1486/", "https://attack.mitre.org/techniques/T1567/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scoping ransomware encryption and exfiltration

**Goal:** know exactly which systems and data are encrypted, which are intact, and what left
the network, because restore planning, notification and negotiation all depend on it.

## Encryption scope
- Inventory hosts showing the ransom note filename and encrypted extension (EDR file events,
  Velociraptor glob hunt for the note name, file share scans).
- Identify the **deployment method** to predict reach: GPO scheduled task, PsExec, WMI,
  hypervisor-level encryption (ESXi `vmdk` encrypted from the host: every VM on it affected).
- Check encryption completeness: many strains do intermittent/partial encryption of large
  files (first N MB), which affects recovery tooling choices.
- Timeline from the earliest note creation times ($MFT/USN) per host shows propagation order.
- Confirm backup repositories, snapshots (VSS deletion events, `vssadmin delete shadows`),
  and hypervisor snapshots status.

## Exfiltration scope
- Look for staging: archives (7z, rar, zip) in unusual paths, `rclone.conf`, MEGAsync,
  WinSCP/FileZilla logs, `Restic`, custom exfil tools (StealBit, ExMatter).
- Network: large outbound transfers in firewall/NetFlow/proxy logs to cloud storage or VPS
  IPs; DNS for mega.nz, file-sharing domains; byte counts per destination.
- Correlate staging paths with file share access logs to list which folders were taken.
- Monitor the group's leak site for proof-pack files; compare to your file listings.

## Output
Two lists for the IC and counsel: encrypted assets (with restore source) and data sets
likely exfiltrated (with confidence and evidence). These drive breach notification analysis.

## Gotchas
- "No exfil found" with no egress logging is "unknown", not "none".
- Encrypted files on shares hosted on an un-encrypted file server: the encrypting host is
  the client, look there for the binary.

## Verify
Spot-check encrypted vs intact status on sample hosts manually and reconcile exfil volume
estimates across at least two sources (proxy and firewall, or NetFlow and EDR).
