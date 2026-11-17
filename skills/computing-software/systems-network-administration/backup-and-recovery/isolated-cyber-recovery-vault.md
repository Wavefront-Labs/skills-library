---
id: computing-software.systems-network-administration.backup-and-recovery.isolated-cyber-recovery-vault
name: isolated-cyber-recovery-vault
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [cyber-vault, cyber-recovery-vault, air-gap, isolated-recovery-environment, ransomware-resilience]
level: advanced
status: draft
description: "Design an isolated cyber recovery vault: operational air gap, separate identity, immutable copies, scanning, a clean room for recovery, and regular drills."
sources:
  - https://www.dell.com/en-us/dt/data-protection/cyber-recovery-solution.htm
  - https://www.cisa.gov/stopransomware/ransomware-guide
  - https://www.ncsc.gov.uk/blog-post/offline-backups-in-an-online-world
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Isolated cyber recovery vault

**Purpose:** a last good copy that survives total compromise of production and the normal backup system, including domain admin and backup admin credentials.

## Properties
1. **Isolation**: separate network segment; replication link opened only on a schedule by the vault side (pull), closed otherwise (operational air gap). No inbound management from production.
2. **Separate identity**: vault systems not joined to production AD; local accounts or a vault-only directory; MFA with separate tokens; no shared passwords.
3. **Immutability**: locked copies (Retention Lock Compliance, object lock compliance mode, WORM) inside the vault.
4. **Analysis**: scan copies for corruption or encryption indicators (entropy analysis, CyberSense-type tools, malware scanners) before marking a point as known-good.
5. **Clean room / isolated recovery environment**: compute, network and tooling inside the vault to restore and validate critical systems (AD, core apps) before reconnecting.

## Products
Dell PowerProtect Cyber Recovery, Rubrik/Cohesity vault offerings, Veeam with hardened repository and isolated infrastructure, cloud accounts with separate org and object lock as a logical vault.

## What to vault
Critical tier: identity (AD system state, Entra config), core databases, application binaries and configs, IaC repos, key material and runbooks.

## Operations
- Physical and logical access limited to a small named group, dual control for changes.
- Drill at least yearly: recover AD and one critical app in the clean room within target time.

## Gotchas
- A vault that uses production DNS, NTP or authentication is not isolated.
- Unscanned copies may hold dormant malware; keep enough history (weeks) to go back before dwell time.

## Verify
Pen test from production cannot reach vault management; a drill restores and validates AD in the clean room.
