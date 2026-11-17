---
id: computing-software.cybersecurity-defensive.threat-intelligence.osint-collection
name: osint-collection
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [osint-collection, intelligence-lifecycle, osint, collection-management, opsec, source-reliability]
level: practitioner
status: draft
description: "Collect open-source intelligence for CTI: source selection, collection tooling, operational security (sock puppets, isolation), recording provenance and legal limits."
sources: ["https://www.sans.org/white-papers/", "https://www.bellingcat.com/category/resources/how-tos/", "https://csrc.nist.gov/pubs/sp/800/150/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# OSINT collection

## Source types
Vendor and government reports (CISA, NCSC, vendor blogs), vulnerability and exploit sources
(NVD, KEV, GitHub PoCs, exploit-db), social media and researcher communities (Mastodon, X, Bluesky,
Telegram channels), code repositories, paste sites, passive DNS/WHOIS/certificate transparency,
internet scan data (Shodan, Censys), malware repositories (MalwareBazaar, VirusTotal), news.

## Collection management
- Tie every source to PIRs in the collection plan; record why you collect it.
- Automate with RSS/feeds into a reader or TIP (Feedly, MISP RSS, OpenCTI connectors), keyword
  monitors for your organisation, products and sector.
- Record provenance: URL, retrieval time, archived copy (archive.org or local snapshot + hash),
  source reliability rating.

## OPSEC
- Use isolated browsing environments (VM or remote browser isolation) and non-attributable
  infrastructure for touching adversary-controlled sites.
- Research personas (sock puppets) only under an approved policy; no interaction that could be
  entrapment or participation in crime.
- Do not download malware or leaked data to corporate endpoints; use the malware lab.

## Legal and ethical
- Respect terms of service and privacy law; accessing stolen data or closed criminal forums needs
  legal sign-off (often outsourced to specialised vendors).
- Keep personal data minimisation in mind when collecting about individuals.

## Gotchas
- Echo chambers: many reports recycle the same original source; trace to primary sources before
  counting as corroboration.
- Social media claims need verification; screenshot and archive before deletion.

## Verify
Collection plan with sources mapped to PIRs, provenance records for intel used in products, OPSEC
policy acknowledged by analysts.
