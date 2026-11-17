---
id: computing-software.cybersecurity-defensive.threat-intelligence.sanitising-intel-before-sharing
name: sanitising-intel-before-sharing
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [information-sharing, sharing-sanitisation, tlp, pii-removal, victim-data, ioc-sharing-hygiene, nist-800-150]
level: practitioner
status: draft
description: "Prepare incident data for external sharing: strip victim and internal identifiers, keep what defenders need, set TLP and PAP, and get the right approvals before release."
sources: ["https://csrc.nist.gov/pubs/sp/800/150/final", "https://www.first.org/tlp/", "https://www.misp-project.org/taxonomies.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sanitising intel before sharing

Sharing helps peers defend themselves, but raw incident data contains your internal details, victims'
personal data and things legal has not cleared. NIST SP 800-150 covers establishing sharing and handling.

## Remove or generalise
- Internal hostnames, IPs, usernames, email addresses of staff, file paths with user names, internal URLs.
- Victim/customer identities and any personal data (names in phishing lures, email recipients).
- Your security tooling details if they reveal gaps ("our EDR missed X on unpatched host Y").
- Attachments with real data (exfil samples, documents): share hashes, not files, unless the recipient
  has a malware-handling agreement.
- Anything under legal hold or law enforcement request not to disclose.

## Keep (what defenders need)
- Attacker indicators: external IPs, domains, URLs, hashes, email sender infrastructure, user agents,
  JA4, certificate fingerprints, with first/last seen times.
- TTPs mapped to ATT&CK with procedure detail (commands with internal values replaced: `net group "Domain Admins" /domain`
  is fine; `\\FS-PAYROLL-01\share` becomes `\\<file-server>\share`).
- Detection content: Sigma/YARA/Suricata rules you wrote.
- Context: sector, initial access vector, timeline (relative or dated), confidence levels.

## Markings
- **TLP 2.0**: `TLP:CLEAR`, `TLP:GREEN`, `TLP:AMBER` (limited to recipient org and its clients),
  `TLP:AMBER+STRICT` (recipient org only), `TLP:RED` (named recipients only).
- **PAP** (Permissible Actions Protocol, MISP taxonomy): what recipients may do with the indicators
  (PAP:CLEAR to PAP:RED, e.g. RED = no active actions that could alert the adversary).
- Confidence and source reliability (admiralty code) where your community uses it.

## Approval workflow
Analyst drafts -> peer check for leakage -> legal/privacy review for incidents involving personal data or
regulators -> communications approval if attributable to your organisation -> share via the agreed channel
(ISAC portal, MISP sharing group). Anonymous submission via the ISAC if attribution is sensitive.

## Gotchas
- Metadata leaks: document properties, PDF author fields, screenshots showing internal consoles.
- Defanging for human readers (`hxxp://`, `[.]`) but machine-readable STIX/MISP keeps real values with TLP.
- Sharing too late loses most of the value; pre-agree what can be shared quickly (IOCs) versus later (narrative).

## Verify
A second analyst searches the package for internal domain names, RFC1918 addresses, staff email patterns and
personal names before release; zero hits.
