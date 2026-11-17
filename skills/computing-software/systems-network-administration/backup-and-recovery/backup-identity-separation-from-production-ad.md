---
id: computing-software.systems-network-administration.backup-and-recovery.backup-identity-separation-from-production-ad
name: backup-identity-separation-from-production-ad
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-domain-separation, backup-server-hardening, ransomware-resilience, immutable-backup, active-directory, mfa]
level: advanced
status: draft
description: "Keep backup infrastructure out of reach of a compromised production domain: separate identity, credentials and MFA, network isolation, and no shared admins."
sources:
  - https://www.cisa.gov/stopransomware/ransomware-guide
  - https://helpcenter.veeam.com/docs/backup/vsphere/best_practices_analyzer.html?ver=120
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Separating backup identity from production AD

Ransomware operators target backups first, usually with **domain admin** credentials. If
the backup server, repositories and consoles trust the production domain, the attacker owns
your recovery.

## Design principles
- **No production-domain trust**: backup servers, proxies and repositories are either
  workgroup machines or members of a separate management forest with no trust (or a
  one-way trust where production cannot administer management).
- **Unique credentials**: local accounts or management-forest accounts used only for
  backups; never reused passwords; stored in a vault outside production AD.
- **MFA** on backup consoles (Veeam 12.1+ supports MFA for console users; PBS has TOTP/
  WebAuthn; cloud consoles enforce MFA) and **four-eyes authorisation** for deletions where
  available.
- **Network isolation**: backup management interfaces on a dedicated VLAN reachable only
  from PAWs/jump hosts; repositories accept only required ports from proxies.
- **Immutable/offline copy** regardless, because separation can still fail.
- **Monitoring** goes to a SIEM the attacker can't easily reach; alert on job deletions,
  retention changes, encryption disabled, new admin users.

## What still needs production credentials
Backup jobs need credentials **into** production (vCenter, guest OS for app-aware processing,
databases). Use least-privilege service accounts dedicated to backup, and assume they may be
compromised: they must not grant rights over the backup system itself.

## Hardened repository pattern
Linux hardened repo (Veeam) or PBS with single-use credentials for initial setup, SSH
disabled afterwards, immutability flags (XFS + chattr), local-only root access via console.

## Gotchas
- Convenience joins ("just add the backup server to the domain for SSO") quietly undo this.
- Hypervisor-level admin (vCenter SSO tied to AD) can delete backup VMs and datastores:
  keep repositories off the production hypervisor/storage when possible.
- Shared out-of-band (iDRAC/iLO) passwords across production and backup hardware.

## Verify
Tabletop: "attacker has Domain Admin and vCenter admin": walk through whether they can
delete backups, change retention, or wipe repositories. Every "yes" is a fix item.
