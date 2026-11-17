---
id: computing-software.digital-forensics-incident-response.incident-response-process.choosing-a-containment-strategy
name: choosing-a-containment-strategy
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [containment-strategy, containment, watch-and-learn, incident-response, nist-sp-800-61, dfir]
level: advanced
status: draft
description: "Choose a containment strategy and its timing: immediate versus delayed, watch-and-learn risks, coordinated containment, and criteria from NIST SP 800-61."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://csrc.nist.gov/pubs/sp/800/61/r3/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing a containment strategy

**Goal:** stop the damage without destroying evidence or tipping off the attacker into a
destructive response, at a time you choose.

## NIST criteria (SP 800-61r2 3.3.1)
Potential damage and theft of resources, need for evidence preservation, service
availability, time and resources to implement, effectiveness (partial or full), and
duration (emergency workaround vs permanent).

## Options
| Strategy | When |
|---|---|
| **Immediate** isolate/disable | Destructive or fast-moving activity (ransomware staging, active exfiltration, wiper), single commodity infection |
| **Delayed, coordinated** containment | Hands-on-keyboard intruder with multiple footholds and persistence; act everywhere at once after scoping |
| **Watch and learn** (monitor only) | Rare; only with legal/exec approval, strong monitoring, and no ongoing harm. Liability if data is lost while watching |

## Coordinated containment pattern
1. Scope first: hosts, accounts, persistence, C2 channels (EDR sweeps, Velociraptor hunts).
2. Prepare all actions in advance: isolation list, account disable list, firewall/DNS blocks,
   credential reset plan, cloud key revocation.
3. Execute in a tight window (often minutes), during low business activity, with all
   operators on the bridge.
4. Watch for attacker reaction (new accounts, re-entry attempts) for 72 h.

## Short-term vs long-term containment
Short-term: isolation, blocks, disabling accounts. Long-term: temporary rebuilds, segmented
VLANs, jump-host-only admin, enhanced monitoring while eradication is prepared.

## Gotchas
- Partial containment (isolating one host while the attacker holds domain admin) just
  announces you have seen them.
- Isolation that also cuts your EDR/forensic access; use EDR isolation that keeps the agent
  connected.
- Get memory before containment on key hosts if feasible.

## Verify
After containment: no new C2 connections, no new logons from compromised accounts, no
activity from contained hosts for the agreed period.
