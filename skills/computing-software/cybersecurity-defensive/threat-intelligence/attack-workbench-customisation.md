---
id: computing-software.cybersecurity-defensive.threat-intelligence.attack-workbench-customisation
name: attack-workbench-customisation
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [attack-workbench, attack-mapping, mitre-attack, stix, attack-navigator, threat-intelligence]
level: advanced
status: docs-checked
description: "Run MITRE ATT&CK Workbench to extend ATT&CK with local techniques, groups and notes, collaborate on mappings, and publish custom collections to Navigator and TIPs."
sources: ["https://github.com/center-for-threat-informed-defense/attack-workbench-frontend", "https://github.com/mitre-attack/attack-stix-data"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ATT&CK Workbench

ATT&CK Workbench (Center for Threat-Informed Defense) is a web application to explore, annotate and
extend ATT&CK locally, stored as STIX 2.1.

## Deploy
Docker Compose is the recommended and only officially supported method (see the Deployment Guide linked from the
frontend repo). The frontend, REST API and MongoDB database must all run and reach each other. Import the ATT&CK collection via collection index
URL (`https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/index.json`) and subscribe
for updates.

## Uses
- **Local knowledge**: add notes to techniques (detection guidance specific to your environment),
  create internal groups/intrusion sets for tracked clusters, add campaigns, software and relationships
  (`uses`) from your own incident reporting.
- **Extensions**: new techniques or sub-techniques for platforms/behaviours ATT&CK lacks (use a
  distinct ID prefix), data sources and analytics.
- **Collections**: bundle custom objects as a collection and publish a collection index so other
  Workbench instances or tools (Navigator, TIP) consume them.
- **Updates**: a collection index lets Workbench check whether new releases have been published.

## Integration
- Workbench imports and exports data as STIX collections and collection indexes.
- Keep internal threat actor profiles synchronised with your TIP (single source of truth decision).

## Gotchas
- Custom IDs can collide with future ATT&CK IDs if you mimic the T-number scheme; use a distinct prefix.
- Sharing collections externally: strip internal notes and apply TLP.

## Verify
Workbench shows current ATT&CK version, your local groups with technique relationships, and a
published collection importable into a test Workbench instance.

## Checked
2026-10-28. Confirmed in the attack-workbench-frontend and attack-stix-data READMEs: STIX storage, frontend plus REST API plus MongoDB, Docker Compose as the only officially supported deployment, collections and collection indexes, subscriptions, the ATT&CK collection index.json. Removed: the `attack-workbench-deployment` repo name and compose command, the X1001 ID example, mitreattack-python, review-before-accept claim, dead ctid.mitre.org link.
Method: documentation only; no commands were run.
