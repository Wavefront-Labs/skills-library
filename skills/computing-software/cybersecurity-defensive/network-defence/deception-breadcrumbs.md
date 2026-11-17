---
id: computing-software.cybersecurity-defensive.network-defence.deception-breadcrumbs
name: deception-breadcrumbs
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [deception-breadcrumbs, lures, decoy-credentials, honeytokens, attacker-misdirection, deception, d3fend-decoy]
level: advanced
status: draft
description: "Plant deception breadcrumbs that lead attackers to decoys: fake credentials in memory and files, RDP/SSH history, mapped drives, bookmarks, placed realistically."
sources: ["https://d3fend.mitre.org/technique/d3f:DecoyUserCredential/", "https://engage.mitre.org/", "https://attack.mitre.org/tactics/TA0007/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deception breadcrumbs and lures

Breadcrumbs are small, believable artefacts on real endpoints that point an intruder toward decoys
(honeypots, honey accounts, decoy shares). Any use of them is high-confidence malicious.

## Breadcrumb types
| Breadcrumb | Where | Leads to |
|---|---|---|
| Cached/fake credentials (decoy account injected into LSASS via a deception agent, or saved creds in Credential Manager) | Workstations, jump hosts | Honey account - any auth attempt alerts |
| RDP `.rdp` files / MRU registry entries, PuTTY saved sessions, `~/.ssh/config` and `known_hosts` entries | Admin workstations | Decoy servers |
| Mapped drive / UNC paths in recent files | User profiles | Decoy file share with honey documents |
| Browser saved logins and bookmarks to "admin portals" | Browsers | Decoy web apps |
| Config files with DB connection strings or cloud keys | App servers, repos | Decoy DB / canary cloud key |
| Kerberoastable decoy SPN account | AD | Alerts on TGS request for that SPN (event 4769) |

## Placement principles
- Match local conventions (naming, OS, timestamps); stale-looking but plausible.
- Distribute across the attack paths you expect (BloodHound paths, admin tier crossings).
- Decoys must be isolated and heavily monitored, never production-connected beyond what they need.
- Keep a register (location, type, decoy target) - and exclude breadcrumbs from IT scripts and scans to avoid false alerts.

## Tools
Commercial deception platforms (Acalvio, Attivo/SentinelOne Singularity Identity, Thinkst Canary) deploy
and rotate breadcrumbs automatically; DIY is possible with GPO/scripts plus honey accounts.

## Gotchas
- Breadcrumbs that look fake (obvious "admin_password.txt") are ignored by skilled attackers and triggered by curious staff.
- Legal/HR: inform governance that deception is in use.

## Verify
- [ ] Purple-team exercise: tester following breadcrumbs triggers alerts within minutes.
- [ ] Breadcrumb register current; no false positives from IT tooling.
