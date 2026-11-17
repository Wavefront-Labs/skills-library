---
id: computing-software.systems-network-administration.backup-and-recovery.backup-server-isolation-and-mfa
name: backup-server-isolation-and-mfa
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-server-hardening, four-eyes-authorization, mfa, veeam, ransomware-resilience, privileged-access, backup-immutability]
level: advanced
status: draft
description: "Harden backup servers: separate identity domain, MFA and four-eyes approval for destructive actions, network isolation, credential hygiene and best-practice analysers."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/best_practices_analyzer.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/four_eyes_authorization.html
  - https://www.cisa.gov/stopransomware/ransomware-guide
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backup server isolation and MFA

**Goal:** attackers who own the production domain still cannot delete or encrypt the backups. Ransomware operators target backup consoles first.

## Identity
- Do not join the backup server and repositories to the production Active Directory, or use a separate management forest/workgroup with dedicated admin accounts.
- Enable **MFA** for backup console logins (Veeam v12 supports TOTP MFA for users; other products similar).
- Separate roles: operators who run restores vs administrators who change retention or delete.
- Store service credentials in the product's credential manager; rotate them; no shared passwords with production.

## Four-eyes authorisation
Require a second administrator to approve destructive operations: deleting backups or restore points, removing repositories, changing users and roles. Veeam calls this four-eyes authorization (v12.1+). Pair with alerts to a channel attackers do not control.

## Network
- Backup infrastructure in its own management network; only required ports from production (agents, proxies) inbound.
- No internet browsing or email on backup servers; restrict RDP to a privileged access workstation/bastion with MFA.
- Management interfaces of storage arrays, tape libraries and BMCs isolated too.

## Configuration hygiene
- Run the vendor's security/best-practice analyser (Veeam Security & Compliance Analyzer) and fix findings: disable unused services, enable encryption for configuration backups, keep TLS strict.
- Patch backup software promptly: backup products are on KEV lists.
- Encrypt configuration backups and store them off the backup server.

## Monitoring
Alert on: retention changes, repository removal, mass deletions, new admin users, MFA disabled, jobs disabled.

## Verify
Penetration-test style check: with production domain admin credentials, attempt to log in to or delete backups; it must fail, and the attempt must alert.
