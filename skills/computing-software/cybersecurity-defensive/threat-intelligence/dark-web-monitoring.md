---
id: computing-software.cybersecurity-defensive.threat-intelligence.dark-web-monitoring
name: dark-web-monitoring
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [dark-web-monitoring, intelligence-lifecycle, initial-access-brokers, credential-leaks, digital-risk-protection, cybercrime-forums]
level: advanced
status: draft
description: "Monitor dark web and criminal forums for threats to the organisation: scope, vendor vs in-house, keywords, access broker listings, credential sales, and safe handling."
sources: ["https://www.cisa.gov/topics/cyber-threats-and-advisories", "https://www.enisa.europa.eu/topics/cyber-threats/threats-and-trends", "https://www.sans.org/white-papers/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Dark web monitoring

## What to watch for
- Initial access broker (IAB) listings describing access to your organisation (often anonymised:
  "US healthcare, $500M revenue, Citrix access, domain user") - match on sector, revenue, geography,
  technology.
- Credential and session cookie sales (infostealer logs marketplaces) for your domains and SSO.
- Mentions of your brand, executives, domains, IP ranges, product names in forums and Telegram channels.
- Data for sale or leaked (customer databases, source code), insider recruitment posts.
- Ransomware leak site postings (see leak site monitoring).

## Approach
- Most organisations use vendors (Recorded Future, Flashpoint, Intel 471, KELA, DRP providers) with
  established access and legal frameworks; in-house access to closed forums requires personas, legal
  approval and strict OPSEC.
- Configure keyword lists: domains, brand names, subsidiary names, executives, IP ranges, unique
  product/internal project names, BIN numbers for banks.
- Triage alerts: relevance, credibility of seller, freshness, verification of sample data.

## Response playbooks
- Credential/stealer log hit: force password reset, revoke sessions, investigate the infected device
  (often personal device), check MFA.
- IAB listing likely you: hunt for the described access (VPN accounts, RDP), rotate credentials,
  engage IR if indicators found.
- Data for sale: verify sample with data owners, invoke breach response.

## Gotchas
- Never buy data or access to "verify" without legal approval; it can fund crime and breach sanctions.
- Many claims are recycled old breaches; check dates and samples.

## Verify
Monthly report: alerts received, verified, actions taken; at least one tabletop exercise on an IAB
listing scenario per year.
