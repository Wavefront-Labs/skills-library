---
id: computing-software.cybersecurity-defensive.threat-intelligence.threat-sharing-agreements-and-legal-protections
name: threat-sharing-agreements-and-legal-protections
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [sharing-agreements, information-sharing, tlp, legal-protections, cisa-2015, isac, data-protection]
level: advanced
status: draft
description: "Set up threat intelligence sharing agreements: NDAs and community rules, TLP obligations, antitrust and privacy considerations, and legal protections such as CISA 2015."
sources: ["https://www.cisa.gov/resources-tools/resources/cybersecurity-information-sharing-act-2015-procedures-and-guidance", "https://www.enisa.europa.eu/publications/information-sharing-and-analysis-centres-isacs-cooperative-models", "https://www.first.org/tlp/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sharing agreements and legal protections

## Agreement types
- **Community membership agreements** (ISACs, ISAOs, FIRST): rules on confidentiality, TLP use,
  permitted use of shared data, attribution, liability disclaimers.
- **Bilateral NDAs/MoUs** with peers, suppliers or MSSPs for incident-specific sharing.
- **Data processing terms** when personal data (IP addresses, emails) is shared (GDPR controller-to-
  controller or processor terms).

## Key clauses
Scope of information, permitted uses (defensive only), onward sharing limits (TLP), anonymisation
requirements, retention and deletion, no warranty/liability limits, termination, governing law.

## Legal protections
- **US Cybersecurity Information Sharing Act of 2015 (CISA 2015)**: liability protection for sharing
  cyber threat indicators and defensive measures with federal government (via CISA's portal/AIS) and
  other entities, when personal information not directly related to the threat is removed; antitrust
  exemption for sharing; FOIA exemption and no waiver of privilege for information shared with the
  government. Check current reauthorisation status.
- **EU**: NIS2 encourages information-sharing arrangements (Article 29) with notification to
  authorities; GDPR legitimate interests (Recital 49) supports processing for network security.
- **Antitrust**: share technical threat data, not pricing or commercial strategy; ISAC rules include
  antitrust guidelines.

## Internal process
Legal pre-approval of standard sharing types (IOCs, TTPs), case-by-case approval for incident details;
log what was shared with whom under which agreement.

## Gotchas
- TLP is a marking, not a contract; enforceability comes from community agreements.
- Over-cautious legal positions stop sharing entirely; pre-approved categories keep it flowing.

## Verify
Agreement register with communities, review dates and approved sharing categories; sharing log audits match.
