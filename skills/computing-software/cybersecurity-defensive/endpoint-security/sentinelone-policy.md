---
id: computing-software.cybersecurity-defensive.endpoint-security.sentinelone-policy
name: sentinelone-policy
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [sentinelone-policy, sentinelone, edr-policy, agent-policy, anti-tamper, detect-protect-mode, edr-operations]
level: practitioner
status: draft
description: "Configure SentinelOne agent policy: site/group inheritance, detect vs protect modes, engines, anti-tamper, deep visibility, exclusions modes, and upgrade policies."
sources: ["https://usea1.sentinelone.net/docs", "https://github.com/Sentinel-One/sentinel-one-api-postman"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SentinelOne policy configuration

(Management console docs are behind customer login; names are from the console.)

## Hierarchy
Account -> Site -> Group; policies inherit downward and can be overridden at group level. Use groups for
workstations, servers, critical servers, VDI, pilot. Dynamic groups via filters (OS, tags, AD).

## Mitigation mode
- **Threats** (malicious) and **Suspicious** each set to Detect or Protect.
- Start Threats = Protect, Suspicious = Detect; move Suspicious to Protect for workstations after tuning.
- Protect actions: kill, quarantine, remediate; **rollback** (Windows VSS-based) for ransomware - make sure VSS snapshots are enabled by the agent policy.

## Engines
Static AI, behavioural AI, documents/scripts, lateral movement, exploits, potentially unwanted apps, intrusion detection,
reputation - keep all on; disable only individually with justification.

## Agent hardening
- **Anti-tamper** on (prevents agent stop/uninstall without passphrase).
- Agent UI/notifications as appropriate; local upgrade/uninstall passphrase stored in vault.
- Deep Visibility (EDR telemetry) enabled, with any data-collection exclusions minimal.

## Exclusions
Types: path, file type, certificate signer, hash, browser. Modes for path exclusions:
"Suppress alerts", "Interoperability" (for other security products) and "Performance focus" modes each
reduce protection to a different degree; prefer the least permissive and scope to groups.

## Upgrades
Upgrade policy with maintenance windows, GA vs EA builds, staged by group.

## Gotchas
- Overriding a setting at group level breaks inheritance for that setting; review overrides.
- Rollback needs VSS space and does not cover network shares.

## Verify
- [ ] All groups in Protect for Threats; any Detect-only group justified.
- [ ] Anti-tamper on everywhere; agent version compliance report.
