---
id: computing-software.digital-forensics-incident-response.incident-response-process.rebuild-versus-clean-decision
name: rebuild-versus-clean-decision
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [rebuild-vs-clean, incident-recovery, recovery-planning, eradication, reimaging, dfir]
level: practitioner
status: draft
description: "Decide whether to rebuild or clean a compromised system: decision criteria, tier-0 rules, evidence preservation first, and the rebuild checklist."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rebuild versus clean decision

**Goal:** choose, per system, between removing known malicious artefacts and rebuilding from
trusted media, with a reason you can defend.

## Default rule
**Rebuild** unless you can show the compromise is fully understood and limited to user-level
artefacts you can enumerate. Cleaning is cheaper today and more expensive when you miss
something.

## Rebuild when any is true
- Attacker had administrator/SYSTEM/root on the host.
- Kernel drivers, bootkits, rootkits, or firmware implants suspected.
- Host is tier-0: domain controller, IdP, PKI/CA, PAM, backup server, hypervisor, EDR console.
- Persistence not fully enumerated, or forensic visibility was poor.
- Ransomware executed on it.

## Cleaning may be acceptable when
- Commodity malware with known, documented behaviour, user context only, EDR telemetry
  complete for the whole infection window, and the vendor/analysis lists all artefacts.

## Rebuild checklist
1. Preserve evidence first (image or triage + memory) and record hashes.
2. Build from **known-good** gold images/installation media, not from backups taken during
   dwell time (they may contain the backdoor).
3. Patch fully and apply hardened baseline before network connection.
4. Restore **data** only (not binaries or system state) from a backup verified clean.
5. New credentials for local accounts and service accounts; new certificates.
6. EDR and logging installed before production traffic.

## Domain controllers
Rebuilding DCs in a compromised forest without a forest recovery plan only moves the
problem; for deep AD compromise, follow Microsoft's AD Forest Recovery Guide or build a
new forest and migrate.

## Verify
Rebuilt host passes compromise sweeps, baseline compliance, and a 30-day elevated monitoring
period without attacker indicators.
