---
id: computing-software.systems-network-administration.backup-and-recovery.ransomware-containment-before-recovery
name: ransomware-containment-before-recovery
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [ransomware-containment, ransomware-recovery, isolated-recovery-environment, forensic-preservation, incident-response]
level: advanced
status: draft
description: "Contain ransomware before restoring anything: isolate segments, protect backups, preserve evidence, stop spread via identity and management planes, gate recovery."
sources:
  - https://www.cisa.gov/stopransomware/ransomware-guide
  - https://csrc.nist.gov/pubs/sp/800/61/r3/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ransomware containment before recovery

Restoring into an environment the attacker still controls gets your restored systems
encrypted again. CISA's #StopRansomware guide puts detection/containment before recovery.

## Immediate actions (first hours)
1. **Isolate**: disconnect affected segments at the switch/firewall (not by powering off
   machines, which destroys memory evidence), block internet egress except for IR tooling,
   cut site-to-site VPNs to unaffected sites if spread risk exists.
2. **Protect backups**: disconnect backup repositories from production networks, disable
   remote deletion paths, verify immutable copies are intact, snapshot backup server
   configuration. Change backup admin credentials from a clean device.
3. **Stop management-plane spread**: disable or restrict hypervisor management (vCenter,
   SCVMM), RMM tools, software deployment (ConfigMgr, Intune scripts), GPO edits; attackers use
   these to push encryptors.
4. **Identity**: disable known compromised accounts, block legacy auth, revoke cloud sessions;
   plan krbtgt and privileged resets (once a clean AD is established).
5. **Preserve evidence**: memory captures and disk images of a few representative systems,
   firewall/EDR/proxy/DC logs, ransom note, encrypted file samples; maintain chain of custody.
   Engage IR firm/insurer/legal early (insurance often requires approved vendors).
6. **Report**: law enforcement/national CERT, regulators per obligations.

## Scoping
Determine initial access vector, attacker accounts and persistence (scheduled tasks, services,
new admin accounts, GPO changes, remote tools), dwell time (how far back backups may contain
persistence), and data exfiltration.

## Gate to start recovery
Recovery may begin (in an isolated recovery environment) when:
- Attacker access paths are known and blocked, or recovery happens in a separate clean network.
- A clean restore point is identified (older than first malicious activity, scanned).
- Clean admin workstations and credentials exist.
- Monitoring (EDR, logging) is in place for restored systems.

## Gotchas
- Wiping and restoring immediately destroys evidence needed to find persistence.
- Restoring a domain controller from a backup that contains the attacker's persistence brings
  it back.
- Paying doesn't remove the need for any of this.

## Verify
Containment checklist completed with timestamps and owners; the recovery start decision is
recorded with the evidence for each gate criterion.
