---
id: computing-software.systems-network-administration.backup-and-recovery.ransomware-rebuild-vs-restore-decisions
name: ransomware-rebuild-vs-restore-decisions
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [rebuild-vs-restore, ransomware-recovery, recovery-sequencing, ad-forest-recovery, tier-0-rebuild, clean-room, incident-response]
level: sme
status: draft
description: "Decide what to rebuild versus restore after ransomware: identity and Tier 0 first, persistence risk, data-only restores into clean builds, and sequencing."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-guide
  - https://www.cisa.gov/stopransomware/ransomware-guide
  - https://csrc.nist.gov/pubs/sp/1800/26/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rebuild vs restore after ransomware

**Goal:** recover operations without restoring the attacker's foothold along with the data.

## The core problem
Backups from before encryption may still contain persistence (backdoors, malicious GPOs, scheduled tasks, compromised accounts) planted during dwell time, which can be weeks. Restoring whole systems can re-infect the environment.

## Decision framework
| Component | Default | Why |
|---|---|---|
| Identity (AD, Entra Connect, PKI, PAM) | Recover via forest recovery procedure from a verified-clean backup, or rebuild; reset all privileged credentials, krbtgt twice | Identity compromise grants everything else |
| Hypervisors, backup servers, management planes | Rebuild from vendor media and IaC | Small, standard, high privilege |
| Network devices, firewalls | Reload known-good firmware and configs from version control | Configs are code |
| Application servers (stateless) | Rebuild from images/IaC, redeploy code | Faster and cleaner than restore |
| Databases, file shares, document stores | **Restore data** from the latest clean point into rebuilt servers | Data is irreplaceable; binaries are not |
| Complex legacy servers that cannot be rebuilt | Restore whole system into an isolated network, scan, hunt, patch, harden, then reconnect | Accept risk with controls |

## Sequencing
1. Isolated recovery environment (clean room) and trusted admin workstations.
2. Identity and Tier 0, with credential resets.
3. Core infrastructure (DNS, DHCP, network, virtualisation, backup).
4. Critical business apps in BIA priority order, data restored and validated.
5. Endpoints reimaged.
Each stage: scan restored data/systems against IOCs from the investigation before connecting to the next.

## Inputs you need
Incident response findings (initial access, dwell time, persistence mechanisms, affected accounts), clean restore point identification, BIA priorities, and RTOs adjusted to the real situation.

## Gotchas
- Restoring a DC from before compromise without resetting credentials leaves stolen hashes valid.
- Pressure to "just restore everything" is highest at hour one; agree the framework in advance in the ransomware playbook.

## Verify
Tabletop the framework annually with security, IT and business leaders, and time a rebuild of one Tier 0 component from scratch in a lab.
