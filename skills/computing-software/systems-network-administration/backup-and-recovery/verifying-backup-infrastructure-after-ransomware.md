---
id: computing-software.systems-network-administration.backup-and-recovery.verifying-backup-infrastructure-after-ransomware
name: verifying-backup-infrastructure-after-ransomware
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-integrity-check, ransomware-recovery, backup-security, immutability, malware-scan, clean-room-recovery]
level: advanced
status: draft
description: "Confirm backup systems are clean before restoring after ransomware: audit logs, retention and immutability, admin accounts, malware scans of restore points, clean rebuild."
sources:
  - https://www.cisa.gov/stopransomware/ransomware-guide
  - https://helpcenter.veeam.com/docs/backup/vsphere/av_scan_about.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/malware_detection.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Verifying backup infrastructure is uncompromised

**Goal:** you restore from backups you can trust, using a backup system the attacker no longer controls.

## Assume the backup server was targeted
Attackers routinely log into backup consoles to delete jobs, shorten retention, or wipe repositories before encrypting.

## Check the control plane
- Backup console audit log / session history: deleted jobs or restore points, retention changes, disabled immutability, new users, MFA changes, unusual logins (time, source IP).
- Accounts: compare backup admin accounts and API keys with the known list; check whether the backup server is domain-joined to the compromised AD.
- Host: EDR alerts on the backup server, proxies and repositories; new services, scheduled tasks, remote tools.
- If any doubt: rebuild the backup server clean from install media and restore its **configuration backup** (encrypted, stored offsite), then rescan repositories.

## Check the data plane
- Immutable copies: confirm Object Lock retention dates, hardened repository immutability, tape/offline media intact.
- Repository integrity: health checks / `restic check --read-data` / PBS verify on the restore points you plan to use.
- Malware scan before restore: mount restore points and scan (Veeam Secure Restore with AV, scan backup, YARA rules from the IR team for the strain's tools and persistence); use detected inline entropy/malware events to narrow which points are infected.
- Pick restore points from before the attacker's **initial access** (not just before encryption), using IR's timeline; dwell time is often weeks.

## Restore path
Restore into an isolated clean-room network first, scan and validate, then promote into the rebuilt production environment.

## Gotchas
- Using the compromised domain admin to log into the backup console re-exposes it.
- Restoring the DC from a point after initial access restores the attacker's accounts and GPOs.

## Verify
Documented sign-off by IR lead that the backup platform and chosen restore points are clean, with the evidence (logs reviewed, scans, checks) attached.
