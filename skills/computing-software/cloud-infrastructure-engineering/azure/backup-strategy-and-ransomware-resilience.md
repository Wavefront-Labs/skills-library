---
id: computing-software.cloud-infrastructure-engineering.azure.backup-strategy-and-ransomware-resilience
name: backup-strategy-and-ransomware-resilience
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bcdr-design, ransomware-resilience, backup-strategy, immutable-backup, isolation]
level: sme
status: docs-checked
description: "Design an Azure backup strategy resilient to ransomware: 3-2-1 with immutability, isolated vaults and identities, MUA, monitoring, and tested clean-restore procedures."
sources: ["https://learn.microsoft.com/azure/security/fundamentals/backup-plan-to-protect-against-ransomware", "https://learn.microsoft.com/azure/backup/protect-backups-from-ransomware-faq", "https://learn.microsoft.com/azure/backup/guidance-best-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup strategy and ransomware resilience

**Goal:** be able to restore a clean copy of critical systems even after an attacker gets admin rights.

## Principles
1. **3-2-1**: 3 copies (original plus 2 backups), 2 storage types, 1 off-site; add immutable or offline storage so an attacker cannot erase it.
2. **Isolate**: backups must not be deletable by the identities that run production.
3. **Detect**: alert on backup tampering.
4. **Restore clean**: identify a safe point-in-time image you know is not infected before restoring.

## Azure controls
| Control | Setting |
|---|---|
| Immutability | Use immutable storage and out-of-band steps (MFA or security PIN) before backups can be modified or erased |
| Soft delete | On by default for a new Recovery Services vault; the best-practice page quotes 14 days retention of deleted backup data: check your vault's current setting |
| MUA | Multi-user authorization through a Resource Guard, so critical operations (disable soft delete, stop or delete backups, reduce retention) need separate authorization; keep the Resource Guard with a different team/subscription |
| Cross-region | Cross Region Restore restores Azure VMs to the paired secondary region |
| Identity isolation | Backup admins in a separate group, PIM-only, phishing-resistant MFA, no standing Owner on vault subscriptions |
| Encryption | Customer-managed keys are optional for vaulted backups; protect the key vault |
| Monitoring | Azure Monitor alerts for backup operations; Backup reports via Workbooks |
| Retention | Size it to cover typical dwell time before detection; set it per workload |

## Recovery runbook outline
1. Contain; declare which identities/systems are compromised.
2. Recover identity first (Entra ID, AD DCs from a known-good backup) in an isolated network.
3. Choose recovery points before the earliest indicator of compromise; scan restored data.
4. Restore tier-0 then critical apps into a clean landing zone; rotate all secrets and keys.
5. Reconnect gradually.

## Test
- Isolated restore of a critical app end to end, timed, on a schedule the business agrees; periodic ransomware tabletop.

## Verify
- [ ] Every critical workload: immutable or MUA-protected backups + off-site copy + last successful restore test date in the register.

## Checked
2026-10-28. Confirmed (Learn: security/fundamentals/backup-plan-to-protect-against-ransomware, backup/protect-backups-from-ransomware-faq,
backup/guidance-best-practices): 3-2-1 definition, immutable storage with out-of-band steps, soft delete on by default,
Resource Guard MUA operations, Cross Region Restore to the paired region, optional CMK, safe point-in-time restore.
Corrected: "30+ days enhanced soft delete" (page says 14 days). Removed: "3-2-1-1-0", locked immutable-vault wording,
daily/weekly/monthly retention figures, quarterly/yearly test cadences, Defender/Sentinel analytics claim. Dead source
well-architected/reliability/backup-and-restore (404) dropped.
Method: documentation only; no commands were run.
