---
id: computing-software.cybersecurity-defensive.threat-intelligence.ransomware-group-profiling
name: ransomware-group-profiling
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [ransomware-group-profiling, adversary-profiling, ransomware, raas, threat-actor-tracking, attack-mapping]
level: advanced
status: draft
description: "Profile ransomware groups and affiliates: RaaS structure, initial access methods, tooling, TTPs, extortion tactics, leak site behaviour and defensive priorities."
sources: ["https://www.cisa.gov/stopransomware", "https://attack.mitre.org/groups/", "https://www.ncsc.gov.uk/collection/ransomware"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Ransomware group profiling

## Understand the ecosystem
Ransomware-as-a-service (RaaS): operators provide the locker, leak site and negotiation; affiliates
perform intrusions; initial access brokers sell access. TTPs vary more by **affiliate** than by brand,
and brands rebrand or splinter frequently.

## Profile template
- Names and aliases, active period, rebrand lineage.
- Model: RaaS/closed group, affiliate recruitment, revenue split.
- Initial access: exploited edge devices (CVE list), valid accounts via IABs/infostealers, phishing,
  RDP/VPN brute force, SEO poisoning.
- Post-exploitation tooling: Cobalt Strike/Sliver/Brute Ratel, AnyDesk/ScreenConnect abuse,
  AdFind/SharpHound, Rclone/MEGA for exfiltration, PsExec/GPO for deployment, BYOVD for EDR killing.
- ATT&CK techniques with evidence; time from access to encryption (dwell time).
- Encryption: platforms (Windows, ESXi, Linux), intermittent encryption, extensions, ransom note.
- Extortion: data leak site, DDoS, contacting customers/regulators, auction behaviour.
- Victimology: sectors, revenue, geographies, exclusions (CIS countries).
- Negotiation patterns and decryptor reliability; known free decryptors (nomoreransom.org).

## Sources
CISA #StopRansomware advisories, vendor DFIR reports, leak site monitoring, ransomware trackers
(ransomware.live, ransomlook), ISAC sharing.

## Defensive output
- Prioritised controls: patch the group's exploited CVEs, MFA on remote access, block RMM tools not
  sanctioned, detect exfil tools, protect backups (immutable, offline), ESXi hardening.
- Detections and hunts mapped to the group's techniques; tabletop scenario based on its playbook.

## Gotchas
- Leak site victim counts lag and omit victims who paid.
- Attribution to a brand from encryption artefacts says little about the affiliate's earlier TTPs.

## Verify
Profile reviewed quarterly; each high-relevance group has corresponding detection coverage layer and
control status.
