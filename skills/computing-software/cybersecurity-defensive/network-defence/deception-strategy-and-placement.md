---
id: computing-software.cybersecurity-defensive.network-defence.deception-strategy-and-placement
name: deception-strategy-and-placement
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [deception-technology, deception-strategy, decoy-placement, high-fidelity-alerts, attacker-paths, d3fend-deceive]
level: advanced
status: draft
description: "Plan a deception programme: pick goals, map attacker paths, place decoys and lures where intruders actually look, route alerts, keep decoys believable, and measure value."
sources: ["https://engage.mitre.org/", "https://d3fend.mitre.org/tactic/d3f:Deceive/", "https://canary.tools/help/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deception strategy and placement

Deception works because legitimate users have no reason to touch decoys: every interaction is a
high-fidelity alert. The craft is putting decoys where attackers go and nobody else does.

## Set goals (MITRE Engage: expose, affect, elicit)
- **Expose**: detect intruders early (most organisations start here).
- **Affect**: slow them down or misdirect (tarpits, fake credentials that lead nowhere).
- **Elicit**: learn TTPs (high-interaction environments; needs mature team and legal review).

## Map attacker paths
Use your own incident history, red team reports and ATT&CK: what does an intruder do after landing on a
workstation? Discovery (AD queries, network scans, share browsing), credential access (LSASS, browser
stores, files named passwords), lateral movement (RDP, SMB to servers), cloud key hunting.
Place deception on each step:
| Step | Decoy |
|---|---|
| AD discovery | Honey user with attractive description, fake SPN (Kerberoast bait), fake admin group |
| Credential hunting | Fake credentials in LSASS (credential injection), `passwords.xlsx` canary doc on shares, fake AWS keys in dev repos/home dirs |
| Network scanning | Decoy servers in each server VLAN (OpenCanary, Thinkst Canary) with realistic names and services |
| Lateral movement | RDP/SMB decoys, fake jump host entries in RDP history/`.ssh/config` |
| Data hunting | Canary files in finance/HR shares, fake database connection strings |
| Cloud | Honey IAM keys, decoy S3 bucket with CloudTrail data events alerting |

## Make them believable
Names matching your conventions, realistic OS/services, some age and activity (last logon, file
timestamps), registered in DNS/AD like real assets. Avoid telling everyone in IT exactly where they are
(insider testing value), but register them in the asset inventory with a "decoy" flag so scanners and
admins do not trip them constantly.

## Alert routing
Decoy alerts go straight to high priority in the SOC with a runbook: identify source host/account,
isolate quickly, investigate. Expect very few, mostly true positives (or vulnerability scanners: exclude them).

## Measure
Coverage of attacker steps, time from compromise to decoy trigger in red team/purple team exercises,
false positive rate (should be near zero after tuning).

## Gotchas
- Decoys must never hold real credentials or data, and must not create real attack paths (honey accounts
  with no privileges, disabled interactive logon where possible).
- Unmaintained decoys go stale (old OS, no activity) and become obvious.
- Legal review for elicitation and any interaction with attackers beyond detection.

## Verify
In each red team exercise, at least one decoy triggers along the attacker's path; the alert reaches the
SOC within minutes.
