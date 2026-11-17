---
id: computing-software.cybersecurity-defensive.security-architecture.backup-infrastructure-hardening
name: backup-infrastructure-hardening
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [resilience, backup-hardening, veeam-hardening, backup-credentials, mfa-backup-console, ransomware-resilience, separate-identity]
level: advanced
status: draft
description: "Harden backup systems that ransomware operators target first: separate identity, MFA, network isolation, hardened repositories, four-eyes deletion, and alerting on tampering."
sources: ["https://www.cisa.gov/stopransomware/ransomware-guide", "https://helpcenter.veeam.com/docs/backup/vsphere/best_practices_analyzer.html", "https://learn.microsoft.com/en-us/azure/backup/multi-user-authorization-concept"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backup infrastructure hardening

Attackers delete or encrypt backups before deploying ransomware. Immutable storage helps only if the
attacker cannot reach the backup console with admin rights.

## Identity
- Backup servers and consoles **not joined to the production AD domain** (workgroup or a separate
  management domain). Domain admin compromise must not equal backup admin.
- Dedicated backup admin accounts, MFA on the console (Veeam supports MFA for console users), no
  shared accounts.
- Service accounts used to reach workloads: least privilege, vaulted, rotated; no domain admin
  "because it was easier".

## Network
- Backup servers, proxies and repositories on a dedicated VLAN; inbound management only from PAWs/jump hosts.
- Repositories accept connections only from backup proxies; no SMB shares writable from production.
- Block internet egress from backup infrastructure except update endpoints.

## Storage
- Immutable copy: hardened Linux repository (Veeam XFS with immutability, single-use credentials,
  SSH disabled), S3 Object Lock in compliance mode, tape/offline rotation, or vendor immutable vaults.
- Follow 3-2-1-1-0 (one offline/immutable, zero restore errors verified).
- Separate cloud account/tenant for backup copies with its own root/global admin credentials.

## Destructive operation controls
- Four-eyes / multi-user authorisation for deleting backups or reducing retention (Veeam four-eyes
  authorisation, Azure Backup multi-user authorisation with Resource Guard, Rubrik/Cohesity quorum).
- Soft delete / recycle bin for backup data with retention longer than typical dwell time.

## Hardening the servers
Patch backup software quickly (Veeam CVEs have been exploited for credential theft), remove
unneeded roles, EDR installed, local firewall, disable RDP or restrict it, encrypt configuration
backups with a password stored offline.

## Monitoring
Send backup logs to the SIEM and alert on: job deletion, retention changes, encryption disabled,
new admin users, failed logons to the console, mass job failures, immutability setting changes.

## Gotchas
- Credentials for hypervisor/cloud APIs stored in the backup server are valuable to attackers;
  protect the configuration database.
- Backup admins with full rights to both primary and the immutable copy defeat the separation.

## Verify
Red/purple-team check: with domain admin credentials only, attempt to log in to the backup console and
delete a test job; both must fail. Quarterly restore test from the immutable copy.
