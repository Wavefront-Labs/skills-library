---
id: computing-software.digital-forensics-incident-response.incident-response-process.sharing-incident-indicators-with-isacs-and-peers
name: sharing-incident-indicators-with-isacs-and-peers
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [isac-sharing, information-sharing, misp, stix, indicator-sharing, dfir]
level: practitioner
status: draft
description: "Share incident indicators with ISACs and peers: legal clearance, sanitising victim data, packaging in MISP or STIX 2.1 with TLP and confidence, and handling feedback."
sources: ["https://csrc.nist.gov/pubs/sp/800/150/final", "https://www.misp-project.org/documentation/", "https://oasis-open.github.io/cti-documentation/stix/intro"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharing incident indicators with ISACs and peers

Sharing turns one victim's pain into others' detections (NIST SP 800-150). Done carelessly it leaks victim identity or breaches confidentiality agreements.

## Clearance
- Get Legal approval; in the US, CISA 2015 provides liability protection for sharing cyber threat indicators for a cybersecurity purpose with personal information removed. Check sector rules and contracts (customers' data, IR firm NDAs).
- Decide attribution: share as your organisation, or anonymously via the ISAC's analysts.

## Sanitise
Remove: internal hostnames, internal IPs, usernames, victim email addresses, file paths containing names, document titles. Keep: external IPs and domains, URLs, hashes, mutexes, user-agents, YARA/Sigma rules, TTP descriptions (ATT&CK IDs), timeframes.
Exclude indicators that are shared infrastructure (CDN IPs, Google Drive URLs) or label them clearly with context; they cause false positives across members.

## Package
MISP event (most ISACs run MISP):
- Event info: short description ("Ransomware precursor, Cobalt Strike via SEO-poisoned installer, Oct 2026"), threat level, analysis state.
- Attributes with category/type (`ip-dst`, `domain`, `sha256`), `to_ids` set only for indicators safe to block automatically, comments with context and first/last seen.
- Tags: `tlp:green` (or amber), `misp-galaxy:mitre-attack-pattern=...`, confidence taxonomy.
STIX 2.1 bundles (Indicator objects with patterns, `valid_from`, `confidence`, TLP marking definitions) for TAXII-based communities.

## After sharing
- Watch for sightings and feedback (other members seeing the same infrastructure extends your scoping).
- Update or revoke indicators that turn out false positive; set expiry for IPs.
- Record in the case what was shared, with whom, and under which TLP.

## Gotchas
- Sharing too early (unconfirmed IOCs) burns trust; sharing too late is useless. Aim for confirmed indicators within days.
- Do not share actor-facing details that might tip off an ongoing law-enforcement operation; coordinate.

## Verify
The shared package contains no internal identifiers, every attribute has context and TLP, and the share is logged in the case comms log.
